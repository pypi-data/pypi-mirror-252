from dataclasses import dataclass
from itertools import groupby
from typing import Any, Iterable, Iterator, Optional, Tuple, Union

from sqlalchemy.orm import Session
from type_checker.decorators import enforce_strict_types
from viavi.fiberparse.Data.SORData import NatureEventType

from viavi.fibermark.db_utils.HelperTypesDB import EventProfFormat, EventTypeDatabase
from viavi.fibermark.db_utils.query_helpers import retrieve_info_measure_marking
from viavi.fibermark.notation.helpers import (
    ClassificationMeasureResults,
    Filtering,
    MetricFilter,
    events_that_needs_notation,
    splitter_events,
)
from viavi.fibermark.notation.stats_helpers import (
    DetailedMark,
    MeasureMark,
    StatisticsMeasure,
    calculate_detailed_statistics_measure,
    calculate_statistics_measure,
)
from viavi.fibermark.utils.helpers import sql_alchemy_events_to_python_events
from viavi.fibermark.utils.logging import logger

IteratorMeasureResultsByEventTypeDatabaseOrNatureEventType = Union[
    Iterator[Tuple[NatureEventType, Iterable[EventProfFormat]]],
    Iterator[Tuple[EventTypeDatabase, Iterable[EventProfFormat]]],
]
ClassificationMeasureResultsByEventTypeDatabaseOrNatureEventType = Union[
    dict[EventTypeDatabase, ClassificationMeasureResults], dict[NatureEventType, ClassificationMeasureResults]
]


@dataclass
class DetailedEvents:
    corresponding_reference_events: list[EventProfFormat]
    corresponding_measure_events: list[EventProfFormat]


@enforce_strict_types
@dataclass
class MeasureEventComparison:
    reference_position_meters: list[float]
    measure_position_meters: list[float]
    corresponding_events: DetailedEvents


MeasureEventComparisonByEventTypeDatabaseOrNatureEventType = Union[
    dict[EventTypeDatabase, MeasureEventComparison], dict[NatureEventType, MeasureEventComparison]
]


def compare_event_characteristic_value_to_threshold(
    characteristic_value: Optional[float], threshold: Optional[float]
) -> bool:
    """
    Characteristic value is either one of loss_db or reflectance_db depending on event,
    threshold is an attribute of Filtering class
    """
    if threshold is None:
        # No filtering when treshold is None
        return True
    else:
        # Treshold is not 0, thus null characteristic values are filtered
        if characteristic_value is None:
            return False
        else:
            return characteristic_value >= threshold


def yield_events_filtered_grouped_by_event_types(
    measure_events: list[EventProfFormat],
    filtering: Filtering,
) -> Iterator[Tuple[EventTypeDatabase, Iterable[EventProfFormat]]]:
    """
    Contains filtering logic, yield events iterables grouped by event types
    having filtered events that need notation and do threshold filtering
    """
    filtered_measure_events_that_needs_notation: list[EventProfFormat] = [
        event for event in measure_events if event.db_evt_type in events_that_needs_notation
    ]
    splice_events_filtered = [
        event
        for event in filtered_measure_events_that_needs_notation
        if event.db_evt_type == EventTypeDatabase.Splice
        and compare_event_characteristic_value_to_threshold(event.loss_db, filtering.splice_db_treshold)
    ]
    ghosts_events_filtered = [
        event
        for event in filtered_measure_events_that_needs_notation
        if event.db_evt_type == EventTypeDatabase.Ghost and filtering.show_ghost
    ]
    reflectance_events_filtered = [
        event
        for event in filtered_measure_events_that_needs_notation
        if event.db_evt_type == EventTypeDatabase.Reflection
        and compare_event_characteristic_value_to_threshold(event.reflectance_db, filtering.reflectance_db_treshold)
    ]
    end_of_fiber_events_filtered = [
        event
        for event in filtered_measure_events_that_needs_notation
        if event.db_evt_type == EventTypeDatabase.FiberEnd and filtering.show_fiber_end
    ]

    events_filtered = (
        splice_events_filtered + ghosts_events_filtered + reflectance_events_filtered + end_of_fiber_events_filtered
    )
    events_splitters = [
        event for event in filtered_measure_events_that_needs_notation if event.db_evt_type in splitter_events
    ]
    events_filtered = events_filtered + events_splitters
    filtered_measure_grouped_by_type_of_events = groupby(
        sorted(events_filtered, key=lambda event: event.db_evt_type),
        lambda event: event.db_evt_type,
    )
    return filtered_measure_grouped_by_type_of_events


def yield_events_filtered_grouped_by_nature_event_types(
    measure_events: list[EventProfFormat],
) -> Iterator[Tuple[NatureEventType, Iterable[EventProfFormat]]]:
    """
    Contains filtering logic, yield events iterables grouped by event types
    having filtered events that need notation and do threshold filtering
    """
    events_filtered = [
        event
        for event in measure_events
        if event.nature_evt_type_if_sor in [NatureEventType.cSPLICE, NatureEventType.cREFLECTION]
    ]
    filtered_measure_grouped_by_type_of_nature_events = groupby(
        sorted(events_filtered, key=lambda event: event.nature_evt_type_if_sor),
        lambda event: event.nature_evt_type_if_sor,
    )
    return filtered_measure_grouped_by_type_of_nature_events


def list_events_to_dict_comparison(
    ref_measure_grouped_by_type_of_events: IteratorMeasureResultsByEventTypeDatabaseOrNatureEventType,
    alg_measure_grouped_by_type_of_events: IteratorMeasureResultsByEventTypeDatabaseOrNatureEventType,
    resolution_meters: Optional[float],  # TOD idea: Remove completely use of index_debut_evt ?
    detailed: bool = False,
) -> MeasureEventComparisonByEventTypeDatabaseOrNatureEventType:
    # Filtering event types with only the ones that contains a position and that needs a notation
    dict_comparison_measure_and_ref_per_events: MeasureEventComparisonByEventTypeDatabaseOrNatureEventType = {}
    # Populating for each type of events in reference Events the position of found events
    for ref_event_type, ref_corresponding_events in ref_measure_grouped_by_type_of_events:
        list_ref_corresponding_events = list(ref_corresponding_events)
        dict_comparison_measure_and_ref_per_events.setdefault(
            ref_event_type, MeasureEventComparison([], [], DetailedEvents([], []))
        )
        ref_event_distance_meters = list(
            map(
                lambda ref_event: round(
                    (
                        ref_event.index_debut_evt * resolution_meters
                        if ref_event.index_debut_evt is not None and resolution_meters is not None
                        else ref_event.pos_meters
                    ),
                    1,
                ),
                list_ref_corresponding_events,
            )
        )
        dict_comparison_measure_and_ref_per_events[ref_event_type].reference_position_meters = ref_event_distance_meters
        # Enrich with event info if detailed for use in detailed comparison
        if detailed:
            dict_comparison_measure_and_ref_per_events[
                ref_event_type
            ].corresponding_events.corresponding_reference_events = list_ref_corresponding_events
    # Populating for each type of events in measure Events the position of found events
    for alg_event_type, alg_corresponding_events in alg_measure_grouped_by_type_of_events:
        list_alg_corresponding_events = list(alg_corresponding_events)
        dict_comparison_measure_and_ref_per_events.setdefault(
            alg_event_type, MeasureEventComparison([], [], DetailedEvents([], []))
        )
        alg_event_distance_meters = list(
            map(
                lambda alg_event: round(
                    (
                        alg_event.index_debut_evt * resolution_meters
                        if alg_event.index_debut_evt is not None and resolution_meters is not None
                        else alg_event.pos_meters
                    ),
                    1,
                ),
                list_alg_corresponding_events,
            )
        )
        dict_comparison_measure_and_ref_per_events[alg_event_type].measure_position_meters = alg_event_distance_meters
        if detailed:
            dict_comparison_measure_and_ref_per_events[
                alg_event_type
            ].corresponding_events.corresponding_measure_events = list_alg_corresponding_events
    for event_type in events_that_needs_notation:
        dict_comparison_measure_and_ref_per_events.setdefault(
            event_type, MeasureEventComparison([], [], DetailedEvents([], []))
        )
    return dict_comparison_measure_and_ref_per_events


@enforce_strict_types
def comparison_per_events_of_measure_to_reference(
    ref_measure_events: list[EventProfFormat],
    algorithm_measure_events: list[EventProfFormat],
    treshold_classification_meters: float,
    ref_resolution_cm: Optional[int],  # If not None, compare to index_debut_evt
    metric_filter: MetricFilter,
    compare_nature_events_only: bool,
) -> ClassificationMeasureResultsByEventTypeDatabaseOrNatureEventType:
    resolution_meters = ref_resolution_cm / 100 if ref_resolution_cm is not None else None
    filtering: Filtering = Filtering(metric_filter)
    if compare_nature_events_only:
        ref_measure_grouped_by_type_of_events = yield_events_filtered_grouped_by_nature_event_types(ref_measure_events)
        alg_measure_grouped_by_type_of_events = yield_events_filtered_grouped_by_nature_event_types(
            algorithm_measure_events
        )
    else:
        ref_measure_grouped_by_type_of_events = yield_events_filtered_grouped_by_event_types(
            ref_measure_events, filtering
        )
        alg_measure_grouped_by_type_of_events = yield_events_filtered_grouped_by_event_types(
            algorithm_measure_events, filtering
        )
    dict_comparison_measure_and_ref_per_events: MeasureEventComparisonByEventTypeDatabaseOrNatureEventType = (
        list_events_to_dict_comparison(
            ref_measure_grouped_by_type_of_events,
            alg_measure_grouped_by_type_of_events,
            resolution_meters,
            detailed=True,
        )
    )
    classification_per_event_type: ClassificationMeasureResultsByEventTypeDatabaseOrNatureEventType = {}
    for event_type, measure_comparison in dict_comparison_measure_and_ref_per_events.items():
        list_indexes_true_positives, list_indexes_false_negatives, list_indexes_false_positives = (
            calculate_detailed_statistics_measure(
                measure_comparison.measure_position_meters,
                measure_comparison.reference_position_meters,
                treshold_classification_meters,
            )
        )
        well_found_events: set[EventProfFormat] = set([
            measure_comparison.corresponding_events.corresponding_reference_events[i]
            for i in list_indexes_true_positives
        ])
        missed_events: set[EventProfFormat] = set([
            measure_comparison.corresponding_events.corresponding_reference_events[i]
            for i in list_indexes_false_negatives
        ])
        not_existing_events_found: set[EventProfFormat] = set([
            measure_comparison.corresponding_events.corresponding_measure_events[i]
            for i in list_indexes_false_positives
        ])
        classification_per_event_type[event_type] = ClassificationMeasureResults(
            well_found_events, missed_events, not_existing_events_found
        )
    return classification_per_event_type


@enforce_strict_types
def compare_measure_to_reference(
    ref_measure_events: list[EventProfFormat],
    algorithm_measure_events: list[EventProfFormat],
    treshold_classification_meters: float,
    ref_resolution_cm: int,
    metric_filter: MetricFilter,
) -> DetailedMark:
    # 3 time pulse width meters for classification
    mark_table: dict[str, Any] = {
        "metric_filter": metric_filter.name,
    }
    resolution_meters = ref_resolution_cm / 100
    filtering: Filtering = Filtering(metric_filter)
    ref_measure_grouped_by_type_of_events = yield_events_filtered_grouped_by_event_types(ref_measure_events, filtering)
    alg_measure_grouped_by_type_of_events = yield_events_filtered_grouped_by_event_types(
        algorithm_measure_events, filtering
    )
    # This dict is of type dict[EventTypeDatabase, MeasureEventComparison] necessarly because
    # ref and alg measure are of type Iterator[Tuple[EventTypeDatabase, Iterable[EventProfFormat]]]
    dict_comparison_measure_and_ref_per_events: dict[EventTypeDatabase, MeasureEventComparison] = (
        list_events_to_dict_comparison(
            ref_measure_grouped_by_type_of_events,
            alg_measure_grouped_by_type_of_events,
            resolution_meters,
            detailed=False,
        )
    )
    splitter_statistics = StatisticsMeasure(0, 0, 0)
    overall_statistics = StatisticsMeasure(0, 0, 0)
    for event_type, measure_comparison in dict_comparison_measure_and_ref_per_events.items():
        event_name: str = event_type.name.lower()
        stats_event = calculate_statistics_measure(
            measure_comparison.measure_position_meters,
            measure_comparison.reference_position_meters,
            treshold_classification_meters,
        )
        overall_statistics += stats_event
        if event_type in splitter_events:
            splitter_statistics += stats_event
        else:
            mark_event = {
                f"nb_false_negatives_{event_name}": stats_event.false_negatives,
                f"nb_false_positives_{event_name}": stats_event.false_positives,
                f"nb_true_positives_{event_name}": stats_event.true_positives,
            }
            mark_table.update(mark_event)
    mark_table.update({
        "nb_false_negatives_splitter": splitter_statistics.false_negatives,
        "nb_false_positives_splitter": splitter_statistics.false_positives,
        "nb_true_positives_splitter": splitter_statistics.true_positives,
    })
    # Adding overall mark
    mark_table.update({
        "nb_false_negatives_overall": overall_statistics.false_negatives,
        "nb_false_positives_overall": overall_statistics.false_positives,
        "nb_true_positives_overall": overall_statistics.true_positives,
    })
    # Sum all splices here into a table. With key splitter
    detailed_mark = DetailedMark(**mark_table)
    return detailed_mark


def mark_measure(session: Session, ref_id: int, alg: str, metric_filter: MetricFilter) -> MeasureMark:
    measure_id, ref_measure_events, algorithm_measure_events, treshold_classification_meters, ref_resolution_cm = (
        retrieve_info_measure_marking(session, ref_id, alg)
    )
    ref_measure_events = sql_alchemy_events_to_python_events(ref_measure_events)
    algorithm_measure_events = sql_alchemy_events_to_python_events(algorithm_measure_events)
    detailed_mark_measure = compare_measure_to_reference(
        ref_measure_events, algorithm_measure_events, treshold_classification_meters, ref_resolution_cm, metric_filter
    )
    return MeasureMark(measure_id, treshold_classification_meters, detailed_mark_measure)


def classifier_stats_measure(
    session: Session, ref_id: int, alg: str, metric_filter: MetricFilter, compare_nature_events_only: bool = False
) -> ClassificationMeasureResultsByEventTypeDatabaseOrNatureEventType:
    """
    Calculate classification statistics measures for specified events using the given algorithm.

    Args:
        session (Session): SQLAlchemy session to access the database.
        ref_id (int): Reference ID to identify the dataset.
        alg (str): Algorithm name for which to calculate the measures.
        metric_filter (MetricFilter): Filter for evaluation.
    Returns:
        dict[EventTypeDatabase, ClassificationMeasureResults]:
            A dictionary where keys are EventTypeDatabase objects representing the event types,
            and values are ClassificationMeasureResults objects containing calculated classification measures.
            if compare_nature_events_only is true. Output is dict[NatureEventType, ClassificationMeasureResults]
    """
    measure_id, ref_measure_events, algorithm_measure_events, treshold_classification_meters, ref_resolution_cm = (
        retrieve_info_measure_marking(session, ref_id, alg)
    )
    logger.debug(f"Inspecting measure_id {measure_id}")
    ref_measure_events = sql_alchemy_events_to_python_events(ref_measure_events)
    algorithm_measure_events = sql_alchemy_events_to_python_events(algorithm_measure_events)
    classification_per_event_type = comparison_per_events_of_measure_to_reference(
        ref_measure_events,
        algorithm_measure_events,
        treshold_classification_meters,
        ref_resolution_cm,
        metric_filter,
        compare_nature_events_only,
    )
    return classification_per_event_type
