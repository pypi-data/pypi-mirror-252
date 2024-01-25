from dataclasses import asdict
from typing import Optional

from sqlalchemy import Integer, func
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import cast
from type_checker.decorators import enforce_strict_types

from viavi.fibermark.cli_commands.filtering_helpers import FilterOptions
from viavi.fibermark.db_utils.orm import AlgorithmMark, Mark, Measure, Reference
from viavi.fibermark.db_utils.query_helpers import find_algorithm
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.notation.stats_helpers import AlgoMark, DetailedMark
from viavi.fibermark.utils.fo_eval_helpers import enrich_query_filters
from viavi.fibermark.utils.logging import logger


@enforce_strict_types
def mark_algo(
    session: Session, alg: str, metric_filter: MetricFilter, filter_options: Optional[FilterOptions] = None
) -> AlgoMark:
    algorithm = find_algorithm(session, alg)
    algorithm_id = algorithm.id
    logger.debug("Algorithm evaluation is only done on Non-Regression curves")
    algorithm_marks_query = (
        session.query(
            func.count(Mark.id),
            cast(func.sum(Mark.nb_true_positives_splice).label("total_true_positives_splice"), Integer),
            cast(func.sum(Mark.nb_false_negatives_splice).label("total_false_negatives_splice"), Integer),
            cast(func.sum(Mark.nb_false_positives_splice).label("total_false_positives_splice"), Integer),
            cast(func.sum(Mark.nb_true_positives_reflection).label("total_true_positives_reflection"), Integer),
            cast(func.sum(Mark.nb_false_negatives_reflection).label("total_false_negatives_reflection"), Integer),
            cast(func.sum(Mark.nb_false_positives_reflection).label("total_false_positives_reflection"), Integer),
            cast(func.sum(Mark.nb_true_positives_ghost).label("total_true_positives_ghost"), Integer),
            cast(func.sum(Mark.nb_false_negatives_ghost).label("total_false_negatives_ghost"), Integer),
            cast(func.sum(Mark.nb_false_positives_ghost).label("total_false_positives_ghost"), Integer),
            cast(func.sum(Mark.nb_true_positives_fiberend).label("total_true_positives_fiberend"), Integer),
            cast(func.sum(Mark.nb_false_negatives_fiberend).label("total_false_negatives_fiberend"), Integer),
            cast(func.sum(Mark.nb_false_positives_fiberend).label("total_false_positives_fiberend"), Integer),
            cast(func.sum(Mark.nb_true_positives_splitter).label("total_true_positives_splitter"), Integer),
            cast(func.sum(Mark.nb_false_negatives_splitter).label("total_false_negatives_splitter"), Integer),
            cast(func.sum(Mark.nb_false_positives_splitter).label("total_false_positives_splitter"), Integer),
            cast(func.sum(Mark.nb_true_positives_overall).label("total_true_positives_overall"), Integer),
            cast(func.sum(Mark.nb_false_negatives_overall).label("total_false_negatives_overall"), Integer),
            cast(func.sum(Mark.nb_false_positives_overall).label("total_false_positives_overall"), Integer),
        )
        .join(Mark.measure)
        .join(Reference)
        .filter(Reference.category == "Non-Regression")
        .filter(Measure.algorithm_id == algorithm_id)
        .filter(Mark.metric_filter == metric_filter.name)
    )
    algorithm_marks_query = enrich_query_filters(algorithm_marks_query, filter_options)
    reference_alg = find_algorithm(session, "reference")
    reference_curves_ref_ids = set(
        [measure.reference_id for measure in reference_alg.measures if measure.reference.category == "Non-Regression"]
    )
    measured_curves_ref_ids = set(
        [measure.reference_id for measure in algorithm.measures if measure.reference.category == "Non-Regression"]
    )
    indexes_curves_not_measured_by_alg = reference_curves_ref_ids - measured_curves_ref_ids
    if len(indexes_curves_not_measured_by_alg) > 0:
        logger.info(f"Non-Regression Curves not measured by algorithm are {indexes_curves_not_measured_by_alg}")
    if algorithm_marks_query is None:
        logger.critical("Could not retrieve any mark")
        raise IndexError(f"No mark in DB to calculate {alg} Note")
    (
        curve_count_for_mark_calculation,
        nb_true_positives_splice,
        nb_false_negatives_splice,
        nb_false_positives_splice,
        nb_true_positives_reflection,
        nb_false_negatives_reflection,
        nb_false_positives_reflection,
        nb_true_positives_ghost,
        nb_false_negatives_ghost,
        nb_false_positives_ghost,
        nb_true_positives_fiberend,
        nb_false_negatives_fiberend,
        nb_false_positives_fiberend,
        nb_true_positives_splitter,
        nb_false_negatives_splitter,
        nb_false_positives_splitter,
        nb_true_positives_overall,
        nb_false_negatives_overall,
        nb_false_positives_overall,
    ) = algorithm_marks_query.first()
    info_message = (
        f"For metric {metric_filter}, Found {curve_count_for_mark_calculation} measures out of"
        f" {len(reference_curves_ref_ids)}"
    )
    if curve_count_for_mark_calculation != 0 and curve_count_for_mark_calculation != len(reference_curves_ref_ids):
        logger.warning(info_message + ", please add missing measures to have a more complete algorithm notation")
    elif curve_count_for_mark_calculation == 0:
        raise IndexError(f"0 measures found for alg {alg}, cannot calculate mark")
    else:
        logger.debug(info_message)
    detailed_mark = DetailedMark(
        metric_filter.name,
        nb_true_positives_splice,
        nb_false_negatives_splice,
        nb_false_positives_splice,
        nb_true_positives_reflection,
        nb_false_negatives_reflection,
        nb_false_positives_reflection,
        nb_true_positives_ghost,
        nb_false_negatives_ghost,
        nb_false_positives_ghost,
        nb_true_positives_splitter,
        nb_false_negatives_splitter,
        nb_false_positives_splitter,
        nb_true_positives_fiberend,
        nb_false_negatives_fiberend,
        nb_false_positives_fiberend,
        nb_true_positives_overall,
        nb_false_negatives_overall,
        nb_false_positives_overall,
    )
    return AlgoMark(algorithm_id, curve_count_for_mark_calculation, indexes_curves_not_measured_by_alg, detailed_mark)


@enforce_strict_types
def upsert_mark_algo(session: Session, alg: str, metric_filter: MetricFilter) -> AlgoMark:
    try:
        algo_mark = mark_algo(session, alg, metric_filter)
        items_mark_algorithm_table = {
            "algorithm_id": algo_mark.algorithm_id,
            "curve_count_for_mark_calculation": algo_mark.curve_count_for_mark_calculation,
            "indexes_curves_not_measured_by_alg": str(algo_mark.indexes_curves_not_measured_by_alg),
        }
        items_mark_algorithm_table.update(asdict(algo_mark.detailed_mark))
        algorithms_marks_insertion_query = (
            insert(AlgorithmMark).values(items_mark_algorithm_table).on_duplicate_key_update(items_mark_algorithm_table)
        )
        session.execute(algorithms_marks_insertion_query)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.fatal("Cannot calculate mark for algorithm")
        raise e
    return algo_mark
