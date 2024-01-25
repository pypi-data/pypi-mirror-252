from typing import Optional

from sqlalchemy.orm import Session
from type_checker.decorators import enforce_strict_types

from viavi.fibermark.cli_commands.filtering_helpers import FilterOptions
from viavi.fibermark.db_utils.orm import (
    Algorithm,
    AlgorithmMark,
    Event,
    Mark,
    Measure,
    Reference,
)
from viavi.fibermark.notation.helpers import ExtractedInfoMeasureMarking, MetricFilter
from viavi.fibermark.notation.threshold import (
    estimate_threshold_classification_from_pulse_and_resolution,
)
from viavi.fibermark.utils.fo_eval_helpers import enrich_query_filters
from viavi.fibermark.utils.helpers import batch_query_result_to_printable_data
from viavi.fibermark.utils.logging import logger


@enforce_strict_types
def find_algorithm(session: Session, alg: str) -> Algorithm:
    """_summary_

    Args:
        alg (str): part of algorithm name

    Returns:
        Algorithm if it did not fail
    """
    algorithms = session.query(Algorithm)
    algo_of_interest = algorithms.filter(Algorithm.name == alg).first()
    if algo_of_interest:
        logger.debug(f"Showing data of algorithm {algo_of_interest.name}\n")
    else:
        algorithm_data = batch_query_result_to_printable_data(algorithms.all())
        logger.warning(
            f"Not found {alg} in algorithm list, algorithms are {[algorithm['name'] for algorithm in algorithm_data]}"
        )
        raise IndexError(f"Algorithm {alg} not found")
    return algo_of_interest


@enforce_strict_types
def select_measure(session: Session, ref_id: Optional[int], alg: str) -> Measure:
    algorithm_id = find_algorithm(session, alg).id
    meas = (
        session.query(Measure)
        .filter(Measure.reference_id == ref_id)
        .filter(Measure.algorithm_id == algorithm_id)
        .first()
    )
    if meas is None:
        logger.fatal(f"Cannot find measure/mark for alg {alg} for --ref-id {ref_id}")
        raise IndexError(f"Measure for alg {alg} and ref-id {ref_id} does not exist")
    return meas


@enforce_strict_types
def select_algo_mark(session: Session, alg: str, metric_filter: MetricFilter) -> AlgorithmMark:
    algorithm_id = find_algorithm(session, alg).id
    alg_mark = (
        session.query(AlgorithmMark)
        .filter(AlgorithmMark.algorithm_id == algorithm_id)
        .filter(AlgorithmMark.metric_filter == metric_filter.name)
        .first()
    )
    if alg_mark is None:
        logger.critical(f"Could not retrieve algo mark for {alg} and metric_filter {metric_filter}")
        raise IndexError(f"Could not find algorithm mark for {algorithm_id} and metric_filter {metric_filter}")
    return alg_mark


@enforce_strict_types
def select_mark(session: Session, ref_id: Optional[int], alg: str, metric_filter: MetricFilter) -> Mark:
    algorithm_id = find_algorithm(session, alg).id
    mark = (
        session.query(Mark)
        .join(Mark.measure)
        .filter(Measure.algorithm_id == algorithm_id)
        .filter(Measure.reference_id == ref_id)
        .filter(Mark.metric_filter == metric_filter)
        .first()
    )
    if mark is None:
        logger.critical(f"Could not retrieve mark for {alg} ref-id {ref_id} and metric_filter {metric_filter}")
        raise IndexError(f"No mark found for metric {metric_filter} and ref-id {ref_id}")
    return mark


@enforce_strict_types
def retrieve_ref_ids_measured_by_algorithm(session: Session, alg: str, filter_options: FilterOptions) -> list[int]:
    algorithm = find_algorithm(session, alg)
    ref_selection_query = session.query(Reference.id).join(Measure).filter(Measure.algorithm_id == algorithm.id)
    ref_selection_query = enrich_query_filters(ref_selection_query, filter_options)
    reference_ids = list(
        map(
            lambda ref_id_tuple: ref_id_tuple[0],
            ref_selection_query,
        )
    )
    return reference_ids


@enforce_strict_types
def retrieve_info_measure_marking(session: Session, ref_id: int, alg: str) -> ExtractedInfoMeasureMarking:
    algorithm_id = find_algorithm(session, alg).id
    measurement_reference = (
        session.query(Measure).filter(Measure.algorithm_id == 1).filter(Measure.reference_id == ref_id).first()
    )
    if measurement_reference:
        logger.debug(f"Reference measure for --ref_id {ref_id} at id {measurement_reference.id} has been found")
        ref_measure_events: list[Event] = measurement_reference.events
        ref_pulse_ns: Optional[int] = measurement_reference.reference.pulse_ns  # For multipulse msor, it is None
        ref_resolution_cm: Optional[int] = (
            measurement_reference.reference.resolution_cm
        )  # For multiresolution msor, it is None
    else:
        logger.fatal(f"Measure for reference --ref_id {ref_id} could not be found")
        raise IndexError(f"Could not fin measure for reference and ref-id {ref_id}")
    measurement_algorithm = (
        session.query(Measure)
        .filter(Measure.algorithm_id == algorithm_id)
        .filter(Measure.reference_id == ref_id)
        .first()
    )
    if measurement_algorithm:
        logger.debug(f"Measure for --ref_id {ref_id} for algorithm id {algorithm_id} has been found")
        algorithm_measure_events: list[Event] = measurement_algorithm.events
    else:
        logger.fatal(f"Measure for reference --ref_id {ref_id} and algorithm id {algorithm_id} could not be found")
        raise IndexError(f"Could not fin measure for alg {alg} and ref-id {ref_id}")
    measure_id = measurement_algorithm.id
    if ref_pulse_ns is None:  # Msor file multipulse, typically FTTH
        treshold_classification_meters = 30.0
    else:
        assert ref_resolution_cm is not None, "For monopulse data, resolution should be mono too, please delve further"
        treshold_classification_meters = estimate_threshold_classification_from_pulse_and_resolution(
            ref_pulse_ns, ref_resolution_cm
        )
    return ExtractedInfoMeasureMarking(
        measure_id, ref_measure_events, algorithm_measure_events, treshold_classification_meters, ref_resolution_cm
    )
