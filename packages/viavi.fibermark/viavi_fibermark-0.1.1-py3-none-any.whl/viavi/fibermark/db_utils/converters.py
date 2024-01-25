import typing

from type_checker.decorators import enforce_strict_types

from viavi.fibermark.db_utils.orm import AlgorithmMark, Mark
from viavi.fibermark.notation.stats_helpers import AlgoMark, DetailedMark


def sql_metric_filter_to_string(sql_metric_filter: set[str]):
    assert len(sql_metric_filter) == 1, f"Could not extract metric type {sql_metric_filter} successfully to string"
    metric_type_str = str(list(sql_metric_filter)[0])
    return metric_type_str


@typing.no_type_check  # Sqlalchemy db types are considered different by type hints
@enforce_strict_types  # but at runtime they are python native ones
def algorithm_mark_from_sql_algorithm_mark(sql_algorithm_mark: AlgorithmMark) -> AlgoMark:
    detailed_mark = DetailedMark(
        metric_filter=sql_metric_filter_to_string(sql_algorithm_mark.metric_filter),
        nb_true_positives_splice=sql_algorithm_mark.nb_true_positives_splice,
        nb_false_negatives_splice=sql_algorithm_mark.nb_false_negatives_splice,
        nb_false_positives_splice=sql_algorithm_mark.nb_false_positives_splice,
        nb_true_positives_reflection=sql_algorithm_mark.nb_true_positives_reflection,
        nb_false_negatives_reflection=sql_algorithm_mark.nb_false_negatives_reflection,
        nb_false_positives_reflection=sql_algorithm_mark.nb_false_positives_reflection,
        nb_true_positives_ghost=sql_algorithm_mark.nb_true_positives_ghost,
        nb_false_negatives_ghost=sql_algorithm_mark.nb_false_negatives_ghost,
        nb_false_positives_ghost=sql_algorithm_mark.nb_false_positives_ghost,
        nb_true_positives_splitter=sql_algorithm_mark.nb_true_positives_splitter,
        nb_false_negatives_splitter=sql_algorithm_mark.nb_false_negatives_splitter,
        nb_false_positives_splitter=sql_algorithm_mark.nb_false_positives_splitter,
        nb_true_positives_fiberend=sql_algorithm_mark.nb_true_positives_fiberend,
        nb_false_negatives_fiberend=sql_algorithm_mark.nb_false_negatives_fiberend,
        nb_false_positives_fiberend=sql_algorithm_mark.nb_false_positives_fiberend,
        nb_true_positives_overall=sql_algorithm_mark.nb_true_positives_overall,
        nb_false_negatives_overall=sql_algorithm_mark.nb_false_negatives_overall,
        nb_false_positives_overall=sql_algorithm_mark.nb_false_positives_overall,
    )
    return AlgoMark(
        algorithm_id=sql_algorithm_mark.algorithm_id,
        curve_count_for_mark_calculation=sql_algorithm_mark.curve_count_for_mark_calculation,
        indexes_curves_not_measured_by_alg=eval(sql_algorithm_mark.indexes_curves_not_measured_by_alg),
        detailed_mark=detailed_mark,
    )


@typing.no_type_check  # Sqlalchemy db types are considered different by type hints
@enforce_strict_types  # but at runtime they are python native ones
def detailed_mark_from_sql_mark(sql_mark: Mark) -> DetailedMark:
    return DetailedMark(
        metric_filter=sql_metric_filter_to_string(sql_mark.metric_filter),
        nb_true_positives_splice=sql_mark.nb_true_positives_splice,
        nb_false_negatives_splice=sql_mark.nb_false_negatives_splice,
        nb_false_positives_splice=sql_mark.nb_false_positives_splice,
        nb_true_positives_reflection=sql_mark.nb_true_positives_reflection,
        nb_false_negatives_reflection=sql_mark.nb_false_negatives_reflection,
        nb_false_positives_reflection=sql_mark.nb_false_positives_reflection,
        nb_true_positives_ghost=sql_mark.nb_true_positives_ghost,
        nb_false_negatives_ghost=sql_mark.nb_false_negatives_ghost,
        nb_false_positives_ghost=sql_mark.nb_false_positives_ghost,
        nb_true_positives_splitter=sql_mark.nb_true_positives_splitter,
        nb_false_negatives_splitter=sql_mark.nb_false_negatives_splitter,
        nb_false_positives_splitter=sql_mark.nb_false_positives_splitter,
        nb_true_positives_fiberend=sql_mark.nb_true_positives_fiberend,
        nb_false_negatives_fiberend=sql_mark.nb_false_negatives_fiberend,
        nb_false_positives_fiberend=sql_mark.nb_false_positives_fiberend,
        nb_true_positives_overall=sql_mark.nb_true_positives_overall,
        nb_false_negatives_overall=sql_mark.nb_false_negatives_overall,
        nb_false_positives_overall=sql_mark.nb_false_positives_overall,
    )
