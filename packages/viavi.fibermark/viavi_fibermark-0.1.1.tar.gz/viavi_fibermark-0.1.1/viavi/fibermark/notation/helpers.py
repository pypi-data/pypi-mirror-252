from dataclasses import astuple, dataclass, field
from enum import Enum, IntEnum
from typing import Optional

from type_checker.decorators import enforce_strict_types

from viavi.fibermark.db_utils.HelperTypesDB import EventProfFormat, EventTypeDatabase
from viavi.fibermark.db_utils.orm import Event


class ContinueOuterLoop(Exception):
    pass


# Filtering for metric type
class MetricFilter(str, Enum):
    All = "All"
    Auto = "Auto"


class ClassificationResult(IntEnum):
    FN = 0
    FP = 1
    TP = 2


@enforce_strict_types
@dataclass
class Filtering:
    metric_filter: MetricFilter
    # Those attributes are to be verified
    show_ghost: bool = field(init=False)  # Ghosts, True or False in FO, always true in 2 configs
    splice_db_treshold: Optional[float] = field(
        init=False
    )  # Treshold to Event Type Splice, where we look at column loss_db
    reflectance_db_treshold: Optional[float] = field(
        init=False
    )  # Treshold applied to Event Type Reflection, where we look at column reflectance_db
    show_fiber_end: bool = field(init=False)

    def __post_init__(self):
        # In all configs we want to evaluate ghost and fiber ends
        self.show_ghost = True
        self.show_fiber_end = True
        if self.metric_filter == MetricFilter.All:
            self.splice_db_treshold = None
            self.reflectance_db_treshold = None
        elif self.metric_filter == MetricFilter.Auto:
            # Not sure, ask benoit later
            self.splice_db_treshold = 0.05
            self.reflectance_db_treshold = -70


splitter_events = [
    EventTypeDatabase.Splitter,
    EventTypeDatabase.Splitter_1_2,
    EventTypeDatabase.Splitter_1_8,
    EventTypeDatabase.Splitter_1_16,
    EventTypeDatabase.Splitter_1_32,
    EventTypeDatabase.Splitter_1_64,
    EventTypeDatabase.Splitter_1_128,
    EventTypeDatabase.Splitter_2_2,
    EventTypeDatabase.Splitter_2_4,
    EventTypeDatabase.Splitter_2_8,
    EventTypeDatabase.Splitter_2_16,
    EventTypeDatabase.Splitter_2_32,
    EventTypeDatabase.Splitter_2_64,
    EventTypeDatabase.Splitter_2_128,
]

events_that_needs_notation = [
    EventTypeDatabase.Splice,
    EventTypeDatabase.Reflection,
    EventTypeDatabase.Ghost,
    EventTypeDatabase.FiberEnd,
] + splitter_events


def same_event(event: EventProfFormat, event_2: EventProfFormat):
    if event.index_debut_evt is not None and event_2.index_debut_evt is not None:
        return abs(event.index_debut_evt - event_2.index_debut_evt) < 10
    else:
        return (
            abs(event.pos_meters - event_2.pos_meters) < 10
        )  # For multipulse files, index_debut_evt is None. Need to compare to meters


# Need to rewrite for None in index_debut_evt
def find_diff_events_two_lists(
    list_1_events: list[EventProfFormat], list_2_events: list[EventProfFormat]
) -> list[EventProfFormat]:
    events_in_list_1_without_near_events_found_in_list_2 = []
    for list_1_event in list_1_events:
        if not any([same_event(list_1_event, event_2) for event_2 in list_2_events]):
            events_in_list_1_without_near_events_found_in_list_2.append(list_1_event)
    return events_in_list_1_without_near_events_found_in_list_2


def substract_optional_floats(real_1: Optional[float], real_2: Optional[float]) -> Optional[float]:
    if real_1 is None:
        return real_2
    elif real_2 is None:
        return -real_1
    else:
        return real_2 - real_1


@enforce_strict_types
@dataclass
class ExtractedInfoMeasureMarking:
    measure_id: int
    ref_measure_events: list[Event]
    algorithm_measure_events: list[Event]
    treshold_classification_meters: float
    ref_resolution_cm: Optional[int]

    def __iter__(self):
        return iter(astuple(self))


@enforce_strict_types
@dataclass
class ClassificationMeasureResults:
    well_found_events: set[EventProfFormat]
    missed_events: set[EventProfFormat]
    not_existing_events_found: set[EventProfFormat]

    def __iter__(self):
        return iter(astuple(self))
