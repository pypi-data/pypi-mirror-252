import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Optional, Union

import viavi.fiberparse
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session
from type_checker.decorators import enforce_strict_types
from viavi.fiberparse.Data.MSORData import MSORData
from viavi.fiberparse.Data.SORData import SORData, TypeMesure

from viavi.fibermark.db_utils.HelperTypesDB import (
    EventProfFormat,
    event_to_event_db_event_type,
    multipulse_event_to_event_db_event_type,
)
from viavi.fibermark.db_utils.orm import (
    Algorithm,
    Event,
    Mark,
    Measure,
    ParsedSorData,
    Reference,
)
from viavi.fibermark.db_utils.query_helpers import find_algorithm
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.notation.measure import mark_measure
from viavi.fibermark.notation.stats_helpers import MeasureMark
from viavi.fibermark.utils.calculate_md5 import md5
from viavi.fibermark.utils.helpers import (
    recreate_msor_data_other_filename,
    recreate_sor_data_other_filename,
)
from viavi.fibermark.utils.logging import logger
from viavi.fibermark.utils.parser_selector import parse_sor_and_derivatives
from viavi.fibermark.utils.sor_data_converters import (
    CustomJSONEncoder,
    get_items_event_table,
    msor_data_to_reference_table,
    sor_data_to_reference_table,
)


@enforce_strict_types
def upsert_reference_from_sor_data(
    session: Session, sor_filepath: str, ref_id: Optional[int], category: str, sor_data: Union[SORData, MSORData]
) -> int:
    filename = Path(sor_filepath).name
    # If table is empty, query result is None, get attributes goes to default which will lead to an insertion at id = 1
    last_ref_id_db = getattr(session.query(Reference).order_by(Reference.id.desc()).first(), "id", 0)
    reference_same_file_already_existing = session.query(Reference).filter(Reference.md5 == md5(sor_filepath)).first()
    if reference_same_file_already_existing:
        error_message = (
            f"Reference with the exact same md5 as {filename} exist at {reference_same_file_already_existing.id},"
            " nothing to insert"
        )
        logger.fatal(error_message)
        raise AttributeError(error_message)
    if ref_id is None:
        ref_id = last_ref_id_db + 1
        logger.debug(f"Inserting reference at {ref_id} as no reference id was specified")
    if isinstance(sor_data, SORData):
        items_reference_table = sor_data_to_reference_table(sor_filepath, ref_id, category, sor_data)
    elif isinstance(sor_data, MSORData):
        items_reference_table = msor_data_to_reference_table(sor_filepath, ref_id, category, sor_data)
    reference_insertion_query = (
        insert(Reference).values(items_reference_table).on_duplicate_key_update(items_reference_table)
    )
    session.execute(reference_insertion_query)
    return ref_id


@enforce_strict_types
def upsert_mark(session: Session, alg: str, ref_id: int, metric_filter: MetricFilter) -> MeasureMark:
    measure_mark = mark_measure(session, ref_id, alg, metric_filter=metric_filter)
    items_mark_table = {
        "measure_id": measure_mark.measure_id,
        "treshold_classification_meters": measure_mark.treshold_classification_meters,
    }
    items_mark_table.update(asdict(measure_mark.detailed_mark))
    mark_insertion_query = insert(Mark).values(items_mark_table).on_duplicate_key_update(items_mark_table)
    session.execute(mark_insertion_query)
    return measure_mark


@enforce_strict_types
def upsert_measure(session: Session, alg: str, ref_id: int, sor_data: Union[SORData, MSORData]) -> None:
    """Upsert a measure referring to ref_id, generated from SORData, marking it with all known MetricFilter"""
    algorithm_id = find_algorithm(session, alg).id
    try:
        measure_if_already_exist = (
            session.query(Measure)
            .filter(Measure.algorithm_id == algorithm_id)
            .filter(Measure.reference_id == ref_id)
            .first()
        )
        if measure_if_already_exist:
            logger.debug(f"Upserting measure reffering to {ref_id}, measure id is {measure_if_already_exist.id}")
            # Deleting old measure for replacement
            measure_id = measure_if_already_exist.id
            session.query(Event).filter(Event.measure_id == measure_id).delete()
        else:
            # If table is empty, query result is None, thus insert at 1
            measure_id = getattr(session.query(Measure).order_by(Measure.id.desc()).first(), "id", 0) + 1
            logger.debug(f"Measure will be added at id {measure_id}")
        items_measure_table = {
            "id": measure_id,
            "date": date.today().strftime("%Y-%m-%d"),
            "algorithm_id": algorithm_id,
            "reference_id": ref_id,
        }
        measure_insertion_query = (
            insert(Measure).values(items_measure_table).on_duplicate_key_update(items_measure_table)
        )
        session.execute(measure_insertion_query)
        if isinstance(sor_data, SORData):
            resolution_meters = sor_data.resolution_m
            for event in sor_data.events:
                event_converted_for_db: EventProfFormat = event_to_event_db_event_type(event, resolution_meters)
                items_event_table = get_items_event_table(event_converted_for_db, measure_id)
                event_insertion_query = (
                    insert(Event).values(items_event_table).on_duplicate_key_update(items_event_table)
                )
                session.execute(event_insertion_query)
        elif isinstance(sor_data, MSORData):
            if sor_data.multipulse_events is None:
                raise RuntimeError("Multipulse event has not been extracted for MSORData, Cannot upload events to DB")
            if len(sor_data.multipulse_events) > 2:
                raise RuntimeError("Multiple Laser file for this Msor, Please complete implementation")
            given_laser_multipulse_event = list(sor_data.multipulse_events.values())[0]
            for multipulse_event in given_laser_multipulse_event:
                multipulse_event_converted_for_db: EventProfFormat = multipulse_event_to_event_db_event_type(
                    multipulse_event
                )
                items_event_table = get_items_event_table(multipulse_event_converted_for_db, measure_id)
                event_insertion_query = (
                    insert(Event).values(items_event_table).on_duplicate_key_update(items_event_table)
                )
                session.execute(event_insertion_query)
        logger.debug(f"Mark id for this measure will be {measure_id}")
        for metric_filter in MetricFilter:
            upsert_mark(session, alg, ref_id, metric_filter)
    except Exception as e:
        raise e


@enforce_strict_types
def upsert_parsed_sor_data(
    session: Session, sor_filepath: Path, ref_id: int, sor_data: Union[SORData, MSORData]
) -> None:
    if isinstance(sor_data, SORData):
        file_extension = Path(sor_data.filename).suffix
        data_dump = recreate_sor_data_other_filename(sor_data, str(ref_id) + file_extension)
        serialized_data = data_dump.json()
    elif isinstance(sor_data, MSORData):
        file_extension = Path(sor_data.sor_data_list[0].filename).suffix
        data_dump = recreate_msor_data_other_filename(sor_data, str(ref_id) + file_extension)
        serialized_data = None
    try:
        with sor_filepath.open(mode="rb") as binary_file:
            items_parsed_sor_data_table = {
                "reference_id": ref_id,
                "serialized_data": serialized_data if serialized_data is not None else "",
                "fiberparse_ver": viavi.fiberparse.__version__,
                "binary_dump": binary_file.read(),
            }
        sor_data_insertion_query = (
            insert(ParsedSorData)
            .values(items_parsed_sor_data_table)
            .on_duplicate_key_update(items_parsed_sor_data_table)
        )
        session.execute(sor_data_insertion_query)
    except Exception as e:
        raise e


@enforce_strict_types
def write_sor_file_to_database(
    session: Session,
    sor_filepath: str,
    ref_id: Optional[int],
    category: str,
    insert_sor_data: bool = True,
    check_sor_data_has_placed_marker_events: bool = False,
) -> None:
    file_extension = Path(sor_filepath).suffix
    if file_extension not in [".sor", ".msor"]:
        logger.fatal(
            f"Trying to import a not .sor/.csor file, but a {file_extension} file, We do not know how to"
            " note well these curves, thus we do not import it to keep database sane"
        )
        raise Exception(f"Cannot parse {file_extension}")
    filename = Path(sor_filepath).name
    sor_data = parse_sor_and_derivatives(sor_filepath)
    if check_sor_data_has_placed_marker_events:
        if isinstance(sor_data, SORData):
            if not any(event.type_mesure == TypeMesure.eEvtType_SemiAuto for event in sor_data.events):
                logger.warning("Checking if SORData has added markers, did not found any. Not adding event to db")
                return
        if isinstance(sor_data, MSORData):
            logger.fatal("Do not know how to check if MSOR combined table event is from added marker")
            return
    try:
        ref_id = upsert_reference_from_sor_data(session, sor_filepath, ref_id, category, sor_data)
        upsert_measure(session, alg="reference", ref_id=ref_id, sor_data=sor_data)
        if insert_sor_data:
            upsert_parsed_sor_data(session, Path(sor_filepath), ref_id, sor_data)
        logger.info(f"Succeeded in adding {filename} curve to DB at ref-id {ref_id}")
        session.commit()

    except Exception as e:
        session.rollback()
        logger.fatal(f"Cannot insert curve {filename} into DB")
        raise e


@enforce_strict_types
def write_measure_to_database(session: Session, sor_filepath: str, ref_id: int, fo_version: str) -> str:
    sor_data = parse_sor_and_derivatives(sor_filepath)
    try:
        try:
            algorithm = find_algorithm(session, fo_version)
        except Exception:
            logger.info(f"Creating Algorithm FO: {fo_version} as it is not already in DB")
            algorithm_name = fo_version
            algorithm = Algorithm(name=algorithm_name)
            session.add(algorithm)
            session.commit()
        algorithm_id = algorithm.id
        algorithm_name = algorithm.name
        logger.debug(f"Algorithm corresponding to measure is at id {algorithm_id}")
        upsert_measure(session, alg=algorithm_name, ref_id=ref_id, sor_data=sor_data)
        session.commit()
        return algorithm_name
    except Exception as e:
        session.rollback()
        logger.fatal(f"Failure in writing to db, due to error \n {e}")
        raise e
