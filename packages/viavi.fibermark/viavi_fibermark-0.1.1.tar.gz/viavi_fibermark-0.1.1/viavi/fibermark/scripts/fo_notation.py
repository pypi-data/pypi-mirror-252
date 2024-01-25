from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session
from type_checker.decorators import enforce_strict_types

from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.db_utils.HelperTypesDB import EventTypeDatabase
from viavi.fibermark.db_utils.orm import Event, Measure, Reference
from viavi.fibermark.db_utils.query_helpers import find_algorithm


@dataclass
class CurveNotation:
    event_positions: list[float]


@enforce_strict_types
@dataclass
class FONotation:
    fo_version_number: str
    curve_notations: dict[int, CurveNotation]


def retrieve_fo_event_positions(
    session: Session,
    fo_version_number: str,
    event_type: EventTypeDatabase,
    ref_ids: Optional[list[int]] = None,
) -> FONotation:
    algorithm_id = find_algorithm(session, fo_version_number).id
    measurements_query = session.query(Measure).join(Reference).filter(Measure.algorithm_id == algorithm_id)
    if ref_ids is not None:
        measurements = measurements_query.filter(Reference.id.in_(ref_ids)).all()
    else:
        measurements = measurements_query.all()
    splice_positions_per_measurements: dict[int, CurveNotation] = {}
    for measure in measurements:
        splice_events = (
            session.query(Event)
            .filter(Event.measure_id == measure.id)
            .filter(Event.event_type == event_type.name)
            .all()
        )
        splice_positions_per_measurements[measure.reference_id] = CurveNotation(
            list(map(lambda splice_event: float(splice_event.pos_debut_evt_meters__calculated_), splice_events)),
        )
    return FONotation(fo_version_number, splice_positions_per_measurements)


if __name__ == "__main__":
    Fo_note = retrieve_fo_event_positions(prod_db_session, "reference", EventTypeDatabase.Splice, [69])
    print(Fo_note)
