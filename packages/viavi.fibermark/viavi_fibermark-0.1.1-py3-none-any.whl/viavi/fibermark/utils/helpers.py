from typing import Optional

from type_checker.decorators import enforce_strict_types
from viavi.fiberparse.Data.MSORData import MSORData
from viavi.fiberparse.Data.SORData import (
    MethodeMesure,
    NatureEventType,
    SORData,
    TypeMesure,
)

from viavi.fibermark.db_utils.HelperTypesDB import EventProfFormat, EventTypeDatabase
from viavi.fibermark.db_utils.orm import Event


def sqlalchemy_obj_to_dict(obj):
    """Convert an SQLAlchemy object to a dictionary."""
    # Get the column names of the SQLAlchemy object's table
    columns = obj.__table__.columns.keys()
    # Create a dictionary with column names as keys and column values as values
    obj_dict = {col: getattr(obj, col) for col in columns}
    return obj_dict


def batch_query_result_to_printable_data(batch_query_result: list):
    data = []
    for query_result in batch_query_result:
        data_dict = sqlalchemy_obj_to_dict(query_result)
        data.append(data_dict)
    return data


@enforce_strict_types
def sql_alchemy_events_to_python_events(extracted_events_from_db: list[Event]) -> list[EventProfFormat]:
    extracted_events: list[EventProfFormat] = []
    for extracted_event in extracted_events_from_db:
        # Extracted event type is a set of str according to sql db structure
        string_event: str = list(extracted_event.event_type)[0]
        event_type: EventTypeDatabase = eval(f"EventTypeDatabase.{string_event}")
        nature_evt_type_if_sor: Optional[NatureEventType] = None
        if extracted_event.nature_evt_type_if_sor is not None:
            nature_evt_type_if_sor = eval(f"NatureEventType.{extracted_event.nature_evt_type_if_sor}")
        extracted_events.append(
            EventProfFormat(
                db_evt_type=event_type,
                index_debut_evt=extracted_event.index_debut_evt,
                index_fin_evt=extracted_event.index_fin_evt,
                loss_db=extracted_event.loss_db,
                reflectance_db=extracted_event.reflectance_db,
                bilan_db=extracted_event.bilan_db,
                pos_meters=extracted_event.pos_debut_evt_meters__calculated_,
                type_mesure=TypeMesure[str(extracted_event.type_mesure)],
                methode_mesure=MethodeMesure[str(extracted_event.methode_mesure)],
                nature_evt_type_if_sor=nature_evt_type_if_sor,
            )
        )
    return extracted_events


def recreate_sor_data_other_filename(sor_data: SORData, filename: str) -> SORData:
    sor_data_other_filename = sor_data
    sor_data_other_filename.filename = filename
    return sor_data_other_filename


def recreate_msor_data_other_filename(msor_data: MSORData, filename: str) -> MSORData:
    new_sor_data_list = []
    for sor_data in msor_data.sor_data_list:
        new_sor_data = sor_data
        new_sor_data.filename = filename
        new_sor_data_list.append(
            new_sor_data
        )
    return MSORData(sor_data_list=new_sor_data_list, multipulse_events=msor_data.multipulse_events)
