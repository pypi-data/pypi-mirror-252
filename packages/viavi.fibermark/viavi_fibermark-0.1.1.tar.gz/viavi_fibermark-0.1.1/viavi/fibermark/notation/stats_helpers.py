import copy
from dataclasses import astuple, dataclass, field
from typing import Optional, Union

import numpy as np
from type_checker.decorators import enforce_strict_types

from viavi.fibermark.notation.helpers import (
    ContinueOuterLoop,
    substract_optional_floats,
)

Floats = Union[float, np.float32, np.float64]
Ints = Union[int, np.int32, np.int64]
Number = Union[Floats, Ints]


def precision(true_positives: int, false_positives: int) -> Optional[float]:
    try:
        return true_positives / (true_positives + false_positives)
    except ZeroDivisionError:
        return None


def recall(true_positives: int, false_negatives: int) -> Optional[float]:
    try:
        return true_positives / (true_positives + false_negatives)
    except ZeroDivisionError:
        return None


def f_score(precision: Optional[float], recall: Optional[float]) -> Optional[float]:
    if isinstance(precision, float) and isinstance(recall, float) and (precision + recall != 0):
        return 2 * (precision * recall) / (precision + recall)
    else:
        return None


def f_score_from_raw_stats(true_positives: int, false_negatives: int, false_positives: int) -> Optional[float]:
    prec = precision(true_positives, false_positives)
    rec = recall(true_positives, false_negatives)
    return f_score(prec, rec)


@enforce_strict_types
@dataclass
class StatisticsMeasure:
    true_positives: int
    false_negatives: int
    false_positives: int

    def __add__(self, other_stats):
        return StatisticsMeasure(
            true_positives=self.true_positives + other_stats.true_positives,
            false_negatives=self.false_negatives + other_stats.false_negatives,
            false_positives=self.false_positives + other_stats.false_positives,
        )

    def __iter__(self):
        return iter(astuple(self))

    def f_score(self) -> Optional[float]:
        return f_score_from_raw_stats(self.true_positives, self.false_negatives, self.false_positives)

    def precision(self) -> Optional[float]:
        return precision(self.true_positives, self.false_positives)


@enforce_strict_types
@dataclass
class DetailedStatisticsMeasures:
    list_indexes_true_positives: list[int]
    list_indexes_false_negatives: list[int]
    list_indexes_false_positives: list[int]

    def __iter__(self):
        return iter(astuple(self))


@enforce_strict_types
@dataclass
class Interval:
    start: Number
    end: Number
    center: Number = field(init=False)

    def __iter__(self):
        return iter(astuple(self))

    def __post_init__(self):
        self.center = (self.end + self.start) / 2

    def size(self):
        return self.end - self.start


def indexes_non_existing_events_found(
    events_measure_meters: list[float], interval_of_acceptance_reference_events: list[Interval]
) -> list[int]:
    indexes_false_positives = []
    copy_interval_of_acceptance_reference_events = copy.deepcopy(interval_of_acceptance_reference_events)
    for i, measured_event in enumerate(events_measure_meters):
        if not any(
            map(
                lambda interval: interval.start <= measured_event <= interval.end,
                copy_interval_of_acceptance_reference_events,
            )
        ):
            indexes_false_positives.append(i)
        else:
            index_event_closest_to_true_positive_already_found = min(
                range(len(copy_interval_of_acceptance_reference_events)),
                key=lambda i: abs(copy_interval_of_acceptance_reference_events[i].center - measured_event),
            )
            copy_interval_of_acceptance_reference_events.pop(index_event_closest_to_true_positive_already_found)
    return indexes_false_positives


def indexes_events_well_found(
    events_measure_meters: list[float], interval_of_acceptance_reference_events: list[Interval]
) -> list[int]:
    """_summary_

    Args:
        events_measure_meters (list[float]): _description_
        interval_of_acceptance_reference_events (list[Interval]): _description_

    Returns:
        list[int]: indexes of TP events, index refers to list of reference events
    """
    indexes_true_positives = []
    for measured_event in events_measure_meters:
        try:
            for j, interval_foundable_event in enumerate(interval_of_acceptance_reference_events):
                measured_event_in_interval: bool = (
                    interval_foundable_event.start <= measured_event <= interval_foundable_event.end  # type: ignore
                )
                not_already_found: bool = j not in indexes_true_positives
                if not_already_found and measured_event_in_interval:
                    indexes_true_positives.append(j)
                    raise ContinueOuterLoop
        except ContinueOuterLoop:
            continue
    return indexes_true_positives


def transform_ref_events_into_intervals_of_acceptance(
    ref_events_meters: list[float], treshold_classification_meters: float
):
    interval_of_acceptance_reference_events = [
        Interval(ref_event_meter - treshold_classification_meters, ref_event_meter + treshold_classification_meters)
        for ref_event_meter in ref_events_meters
    ]
    return interval_of_acceptance_reference_events


@enforce_strict_types
def calculate_statistics_measure(
    events_measure_meters: list[float], ref_events_meters: list[float], treshold_classification_meters: float
) -> StatisticsMeasure:
    """Please ensure this function is always called with one type of events.

    Args:
        events_measure_meters (list[float]): position of measure events in meters
        ref_events_meters (list[float]): position of reference events in meters
        treshold_classification_meters (float): treshold to classify event as well classified

    Returns:
        StatisticsMeasure: Object containing count of TP, FN, FP
    """
    interval_of_acceptance_reference_events = transform_ref_events_into_intervals_of_acceptance(
        ref_events_meters, treshold_classification_meters
    )
    theoretical_count_events_to_find = len(ref_events_meters)
    false_positives = len(
        indexes_non_existing_events_found(events_measure_meters, interval_of_acceptance_reference_events)
    )
    true_positives = len(indexes_events_well_found(events_measure_meters, interval_of_acceptance_reference_events))
    false_negatives = theoretical_count_events_to_find - true_positives
    return StatisticsMeasure(true_positives, false_negatives, false_positives)


@enforce_strict_types
def calculate_detailed_statistics_measure(
    events_measure_meters: list[float], ref_events_meters: list[float], treshold_classification_meters: float
) -> DetailedStatisticsMeasures:
    """Please ensure this function is always called with one type of events.

    Args:
        events_measure_meters (list[float]): position of measure events in meters
        ref_events_meters (list[float]): position of reference events in meters
        treshold_classification_meters (float): treshold to classify event as well classified

    Returns:
        StatisticsMeasure: Contains:
        - list of indexes of TP (references list indexes) -> Events well found
        - list of indexes of FN (measures list indexes) -> Events found that did not exist
        - list of indexes of FP (references list indexes) -> Events not found in those that exist
    """
    interval_of_acceptance_reference_events = transform_ref_events_into_intervals_of_acceptance(
        ref_events_meters, treshold_classification_meters
    )
    theoretical_count_events_to_find = len(ref_events_meters)
    indexes_false_positives = indexes_non_existing_events_found(
        events_measure_meters, interval_of_acceptance_reference_events
    )
    indexes_true_positives = indexes_events_well_found(events_measure_meters, interval_of_acceptance_reference_events)
    indexes_false_negatives = [i for i in range(theoretical_count_events_to_find) if i not in indexes_true_positives]
    return DetailedStatisticsMeasures(indexes_true_positives, indexes_false_negatives, indexes_false_positives)


@enforce_strict_types
@dataclass
class DiffMarks:
    """
    Diff marks contains fields with mark_2 - mark_1 if both fields are not None,
    else it considers None is 0 and apply the same operation
    """

    diff_nb_true_positives_splice: int
    diff_nb_false_negatives_splice: int
    diff_nb_false_positives_splice: int
    diff_f_score_splice: Optional[float]
    diff_nb_true_positives_reflection: int
    diff_nb_false_negatives_reflection: int
    diff_nb_false_positives_reflection: int
    diff_f_score_reflection: Optional[float]
    diff_nb_true_positives_ghost: int
    diff_nb_false_negatives_ghost: int
    diff_nb_false_positives_ghost: int
    diff_f_score_ghost: Optional[float]
    diff_nb_true_positives_splitter: int
    diff_nb_false_negatives_splitter: int
    diff_nb_false_positives_splitter: int
    diff_f_score_splitter: Optional[float]
    diff_nb_true_positives_fiberend: int
    diff_nb_false_negatives_fiberend: int
    diff_nb_false_positives_fiberend: int
    diff_f_score_fiberend: Optional[float]
    diff_nb_true_positives_overall: int
    diff_nb_false_negatives_overall: int
    diff_nb_false_positives_overall: int
    diff_f_score_overall: Optional[float]


# We use this subclass to implement substraction and comparison on those dataclass
@enforce_strict_types
@dataclass  # Add Splitters here
class DetailedMark:  # Add splitter info here
    metric_filter: str  # Here string name is needed MetricFilter.name (for db insertion compatibility)
    nb_true_positives_splice: int
    nb_false_negatives_splice: int
    nb_false_positives_splice: int
    f_score_splice: Optional[float] = field(init=False)
    nb_true_positives_reflection: int
    nb_false_negatives_reflection: int
    nb_false_positives_reflection: int
    f_score_reflection: Optional[float] = field(init=False)
    nb_true_positives_ghost: int
    nb_false_negatives_ghost: int
    nb_false_positives_ghost: int
    f_score_ghost: Optional[float] = field(init=False)
    nb_true_positives_splitter: int
    nb_false_negatives_splitter: int
    nb_false_positives_splitter: int
    f_score_splitter: Optional[float] = field(init=False)
    nb_true_positives_fiberend: int
    nb_false_negatives_fiberend: int
    nb_false_positives_fiberend: int
    f_score_fiberend: Optional[float] = field(init=False)
    nb_true_positives_overall: int
    nb_false_negatives_overall: int
    nb_false_positives_overall: int
    f_score_overall: Optional[float] = field(init=False)

    def __post_init__(self):
        self.f_score_splice = f_score_from_raw_stats(
            self.nb_true_positives_splice, self.nb_false_negatives_splice, self.nb_false_positives_splice
        )
        self.f_score_reflection = f_score_from_raw_stats(
            self.nb_true_positives_reflection, self.nb_false_negatives_reflection, self.nb_false_positives_reflection
        )
        self.f_score_ghost = f_score_from_raw_stats(
            self.nb_true_positives_ghost, self.nb_false_negatives_ghost, self.nb_false_positives_ghost
        )
        self.f_score_splitter = f_score_from_raw_stats(
            self.nb_true_positives_splitter, self.nb_false_negatives_splitter, self.nb_false_positives_splitter
        )
        self.f_score_fiberend = f_score_from_raw_stats(
            self.nb_true_positives_fiberend, self.nb_false_negatives_fiberend, self.nb_false_positives_fiberend
        )
        self.f_score_overall = f_score_from_raw_stats(
            self.nb_true_positives_overall, self.nb_false_negatives_overall, self.nb_false_positives_overall
        )

    def __sub__(self, other_mark) -> DiffMarks:
        return DiffMarks(
            diff_nb_true_positives_splice=other_mark.nb_true_positives_splice - self.nb_true_positives_splice,
            diff_nb_false_negatives_splice=other_mark.nb_false_negatives_splice - self.nb_false_negatives_splice,
            diff_nb_false_positives_splice=other_mark.nb_false_positives_splice - self.nb_false_positives_splice,
            diff_f_score_splice=substract_optional_floats(self.f_score_splice, other_mark.f_score_splice),
            diff_nb_true_positives_reflection=other_mark.nb_true_positives_reflection
            - self.nb_true_positives_reflection,
            diff_nb_false_negatives_reflection=other_mark.nb_false_negatives_reflection
            - self.nb_false_negatives_reflection,
            diff_nb_false_positives_reflection=other_mark.nb_false_positives_reflection
            - self.nb_false_positives_reflection,
            diff_f_score_reflection=substract_optional_floats(self.f_score_reflection, other_mark.f_score_reflection),
            diff_nb_true_positives_ghost=other_mark.nb_true_positives_ghost - self.nb_true_positives_ghost,
            diff_nb_false_negatives_ghost=other_mark.nb_false_negatives_ghost - self.nb_false_negatives_ghost,
            diff_nb_false_positives_ghost=other_mark.nb_false_positives_ghost - self.nb_false_positives_ghost,
            diff_f_score_ghost=substract_optional_floats(self.f_score_ghost, other_mark.f_score_ghost),
            diff_nb_true_positives_splitter=other_mark.nb_true_positives_splitter - self.nb_true_positives_splitter,
            diff_nb_false_negatives_splitter=other_mark.nb_false_negatives_splitter - self.nb_false_negatives_splitter,
            diff_nb_false_positives_splitter=other_mark.nb_false_positives_splitter - self.nb_false_positives_splitter,
            diff_f_score_splitter=substract_optional_floats(self.f_score_splitter, other_mark.f_score_splitter),
            diff_nb_true_positives_fiberend=other_mark.nb_true_positives_fiberend - self.nb_true_positives_fiberend,
            diff_nb_false_negatives_fiberend=other_mark.nb_false_negatives_fiberend - self.nb_false_negatives_fiberend,
            diff_nb_false_positives_fiberend=other_mark.nb_false_positives_fiberend - self.nb_false_positives_fiberend,
            diff_f_score_fiberend=substract_optional_floats(self.f_score_fiberend, other_mark.f_score_fiberend),
            diff_nb_true_positives_overall=other_mark.nb_true_positives_overall - self.nb_true_positives_overall,
            diff_nb_false_negatives_overall=other_mark.nb_false_negatives_overall - self.nb_false_negatives_overall,
            diff_nb_false_positives_overall=other_mark.nb_false_positives_overall - self.nb_false_positives_overall,
            diff_f_score_overall=substract_optional_floats(self.f_score_overall, other_mark.f_score_overall),
        )


@enforce_strict_types
@dataclass
class AlgoMark:
    algorithm_id: int
    curve_count_for_mark_calculation: int
    indexes_curves_not_measured_by_alg: set[int]
    detailed_mark: DetailedMark


@enforce_strict_types
@dataclass
class MeasureMark:
    measure_id: int
    treshold_classification_meters: float
    detailed_mark: DetailedMark
