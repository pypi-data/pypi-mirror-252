from sqlalchemy.orm import Session
from type_checker.decorators import enforce_strict_types

from viavi.fibermark.db_utils.converters import (
    algorithm_mark_from_sql_algorithm_mark,
    detailed_mark_from_sql_mark,
)
from viavi.fibermark.db_utils.query_helpers import select_algo_mark, select_mark
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.notation.stats_helpers import AlgoMark, DetailedMark, DiffMarks
from viavi.fibermark.utils.logging import logger


@enforce_strict_types
def retrieve_detailed_algo_mark(session: Session, alg: str, metric_filter: MetricFilter) -> AlgoMark:
    sql_algo_mark = select_algo_mark(session, alg, metric_filter)
    algo_mark = algorithm_mark_from_sql_algorithm_mark(sql_algo_mark)
    return algo_mark


@enforce_strict_types
def compare_algos(session: Session, alg_1: str, alg_2: str, metric_filter: MetricFilter) -> DiffMarks:
    algo_mark_1 = retrieve_detailed_algo_mark(session, alg_1, metric_filter)
    algo_mark_2 = retrieve_detailed_algo_mark(session, alg_2, metric_filter)

    if algo_mark_1.indexes_curves_not_measured_by_alg != algo_mark_2.indexes_curves_not_measured_by_alg:
        logger.warning(
            f"Both algorithms do not have the same curves marked, comparison may not make sense \n alg {alg_1} did not"
            f" measure {algo_mark_1.indexes_curves_not_measured_by_alg},  alg {alg_2} did not measure"
            f" {algo_mark_2.indexes_curves_not_measured_by_alg}"
        )
    diff_marks = algo_mark_2.detailed_mark - algo_mark_1.detailed_mark
    return diff_marks


@enforce_strict_types
def retrieve_detailed_mark(session: Session, ref_id: int, alg: str, metric_filter: MetricFilter) -> DetailedMark:
    mark = select_mark(session, ref_id, alg, metric_filter)
    detailed_mark = detailed_mark_from_sql_mark(mark)
    return detailed_mark


@enforce_strict_types
def compare_measures(session: Session, alg_1: str, alg_2: str, ref_id: int, metric_filter: MetricFilter) -> DiffMarks:
    detailed_mark_1 = retrieve_detailed_mark(session, ref_id, alg_1, metric_filter)
    detailed_mark_2 = retrieve_detailed_mark(session, ref_id, alg_2, metric_filter)
    diff_measure_mark = detailed_mark_2 - detailed_mark_1
    return diff_measure_mark
