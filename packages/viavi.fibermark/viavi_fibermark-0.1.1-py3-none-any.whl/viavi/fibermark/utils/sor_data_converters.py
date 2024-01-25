import json
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any

from type_checker.decorators import enforce_strict_types
from viavi.fiberparse.Data.MSORData import MSORData
from viavi.fiberparse.Data.SORData import SORData

from viavi.fibermark.db_utils.HelperTypesDB import EventProfFormat
from viavi.fibermark.utils.calculate_md5 import md5


def construct_remote_storage_path(sor_filepath: str, ref_id: int) -> str:
    return str(ref_id) + Path(sor_filepath).suffix


def get_current_datestring() -> str:
    return date.today().strftime("%Y-%m-%d")


@enforce_strict_types
def sor_data_to_reference_table(sor_filepath: str, ref_id: int, category: str, sor_data: SORData):
    reference_dict = {
        "id": ref_id,
        "path": construct_remote_storage_path(sor_filepath, ref_id),
        "module": sor_data.module_name,
        "date": get_current_datestring(),
        "pulse_ns": sor_data.pulse_ns,
        "acq_range_km": sor_data.acquisition_range_km,
        "laser": sor_data.lambda_nm,
        "resolution_cm": sor_data.resolution_m * 100,
        "acquisition_time_sec": sor_data.acquisition_time_sec,
        "n": sor_data.refractive_index,
        "k": sor_data.k,
        "category": category,
        "noise_floor_db": sor_data.noise_floor_db,
        "md5": md5(sor_filepath),
    }
    return reference_dict


@enforce_strict_types
def msor_data_to_reference_table(sor_filepath: str, ref_id: int, category: str, msor_data: MSORData):
    sor_data_list = msor_data.sor_data_list
    is_multi_pulse = not all(sor_data.pulse_ns == sor_data_list[0].pulse_ns for sor_data in sor_data_list)
    is_multi_acquisition_range_km = not all(
        sor_data.acquisition_range_km == sor_data_list[0].acquisition_range_km for sor_data in sor_data_list
    )
    is_multi_lambda = not all(sor_data.lambda_nm == sor_data_list[0].lambda_nm for sor_data in sor_data_list)
    is_multi_resolution = not all(sor_data.resolution_m == sor_data_list[0].resolution_m for sor_data in sor_data_list)
    is_multi_acquisition_time_sec = not all(
        sor_data.acquisition_time_sec == sor_data_list[0].acquisition_time_sec for sor_data in sor_data_list
    )
    is_multi_noise_floor = not all(
        sor_data.noise_floor_db == sor_data_list[0].noise_floor_db for sor_data in sor_data_list
    )
    reference_dict = {
        "id": ref_id,
        "path": construct_remote_storage_path(sor_filepath, ref_id),
        "module": sor_data_list[0].module_name,  # All acquisition from a file are from Same Module
        "date": get_current_datestring(),
        "pulse_ns": sor_data_list[0].pulse_ns if not is_multi_pulse else None,
        "acq_range_km": sor_data_list[0].acquisition_range_km if not is_multi_acquisition_range_km else None,
        "laser": sor_data_list[0].lambda_nm if not is_multi_lambda else None,
        "resolution_cm": sor_data_list[0].resolution_m * 100 if not is_multi_resolution else None,  # Not all the same
        "acquisition_time_sec": sor_data_list[0].acquisition_time_sec if not is_multi_acquisition_time_sec else None,
        "n": sor_data_list[0].refractive_index,
        "k": sor_data_list[0].k,
        "category": category,
        "noise_floor_db": sor_data_list[0].noise_floor_db if not is_multi_noise_floor else None,
        "md5": md5(sor_filepath),
    }
    return reference_dict


@enforce_strict_types
def get_items_event_table(event: EventProfFormat, measure_id: int) -> dict[str, Any]:
    items_event_table = {
        "measure_id": measure_id,
        "event_type": event.db_evt_type.name,
        "index_debut_evt": event.index_debut_evt,
        "pos_debut_evt_meters (calculated)": event.pos_meters,
        "index_fin_evt": event.index_fin_evt,
        "loss_db": event.loss_db,
        "reflectance_db": event.reflectance_db,
        "bilan_db": event.bilan_db,
        "methode_mesure": event.methode_mesure.name,
        "type_mesure": event.type_mesure.name,
        "nature_evt_type_if_sor": (
            event.nature_evt_type_if_sor.name if event.nature_evt_type_if_sor is not None else None
        ),
    }
    return items_event_table


# Custom JSON encoder for handling non-serializable types
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)
