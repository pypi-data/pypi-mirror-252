from typing import Optional

import click

from viavi.fibermark.cli_commands.filtering_helpers import (
    FilterOptions,
    load_filters_from_json,
)
from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.notation.comparison import compare_algos, compare_measures
from viavi.fibermark.notation.detailed_reports_comparisons import (
    detailed_algo_comparison,
    detailed_algo_comparison_to_ref,
)
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.utils.logging import logger


@click.group()
def compare():
    """
    Compare command group.
    """
    pass


@compare.command()
@click.option("--alg-1", type=str, help="Algorithm name 1", required=True)
@click.option("--alg-2", type=str, help="Algorithm name 2", required=True)
@click.option("--metric-filter", type=click.Choice(MetricFilter), default=MetricFilter.All)  # type: ignore
@click.option(
    "--detailed",
    is_flag=True,
    help='Generate excel report in the form "alg-2 comparison to alg-1.xlsx"',
)
@click.option("--use_filters", type=click.Path(exists=True))
def algos(alg_1: str, alg_2: str, metric_filter: MetricFilter, detailed: bool, use_filters: Optional[str]):
    """Compare two algorithms overall performance for a given metric-filter"""
    logger.info(f"Comparing performance of Algorithm 1: {alg_1}, Algorithm 2: {alg_2}")
    if use_filters is not None:
        filter_options = load_filters_from_json(use_filters)
    else:
        filter_options = None
    if not detailed:
        # Trivial logic, comparing algorithm global marks, or mark on a curve if all measure exists.
        # Warn pb on number of curve from ref used to calculate notes
        diff_marks = compare_algos(prod_db_session, alg_1, alg_2, metric_filter)
        logger.info(f"Diff between algo marks are {diff_marks}")
    else:
        logger.info("Making detailed comparison")
        detailed_algo_comparison(prod_db_session, alg_1, alg_2, filter_options)


@compare.command()
@click.option("--alg", type=str, help="Algorithm name", required=True)
@click.option("--metric-filter", type=click.Choice(MetricFilter), default=MetricFilter.All)  # type: ignore
@click.option("--use_filters", type=click.Path(exists=True))
def algo_to_ref(alg: str, metric_filter: MetricFilter, use_filters: Optional[str]):
    """Compare algorithm to reference for a given metric-filter"""
    logger.info(f"Comparing performance of Algorithm: {alg} to reference")
    if use_filters is not None:
        filter_options = load_filters_from_json(use_filters)
    else:
        filter_options = None
    detailed_algo_comparison_to_ref(prod_db_session, alg, metric_filter, filter_options)


@compare.command()
@click.option("--ref-id", type=int, help="An integer ID", required=True)
@click.option("--alg-1", type=str, help="Algorithm name 1", required=True)
@click.option("--alg-2", type=str, help="Algorithm name 2", required=True)
@click.option("--metric-filter", type=click.Choice(MetricFilter), default=MetricFilter.All)  # type: ignore
def measure(ref_id=int, alg_1=str, alg_2=str, metric_filter=MetricFilter):
    """Compare two measures of two algorithms reffering to --ref-id for a given metric-filter"""
    logger.info(f"Comparing performance of Algorithm 1: {alg_1}, Algorithm 2: {alg_2}")
    logger.warning("Showing only columns who have differences between two algorithms")
    diff_measure_mark = compare_measures(prod_db_session, alg_1, alg_2, ref_id, metric_filter)
    logger.info(f"Diff between measure marks are {diff_measure_mark}")


@click.group()
def nature_events():
    """
    Comparison on nature_events group of command
    (Experimental to help new measure dev)
    """
    pass


@nature_events.command()
@click.option("--alg-1", type=str, help="Algorithm name 1", required=True)
@click.option("--alg-2", type=str, help="Algorithm name 2", required=True)
@click.option("--use_filters", type=click.Path(exists=True))
def algorithms(alg_1: str, alg_2: str, use_filters: Optional[str]):
    if use_filters is not None:
        filter_options = load_filters_from_json(use_filters)
        filter_options.file_extension = ".sor"
    else:
        filter_options = FilterOptions(
            pulse_ns=[], eval_category=["Non-Regression"], files_to_skip=[], eval_only_file=[], file_extension=".sor"
        )
    logger.warning(
        "This function compare Raw measure considering the Meas Table with nature_evt_type, only evaluating .sor files."
        " Be aware notes of algo is relative to Result Table. Detailed excel results is from nature_evt"
    )
    detailed_algo_comparison(prod_db_session, alg_1, alg_2, filter_options, compare_nature_events_only=True)


compare.add_command(nature_events)
