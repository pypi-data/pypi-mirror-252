import click

from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.db_utils.db_insertion import upsert_mark
from viavi.fibermark.notation.algo import upsert_mark_algo
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.utils.logging import logger


@click.group()
def note():
    """
    Note command group.
    """
    pass


@note.command()
@click.option("--alg", type=str, help="Algorithm name", required=True)
@click.option("--metric-filter", type=click.Choice(MetricFilter), default=MetricFilter.All)  # type: ignore
def algo(alg=str, metric_filter=MetricFilter):
    """Note an algorithm"""
    logger.info(f"Noting Algorithm name: whose name contains {alg} with metric {metric_filter}")
    result_algo_mark = upsert_mark_algo(prod_db_session, alg, metric_filter)
    logger.info(f"Algorithm mark is {result_algo_mark}")


@note.command()
@click.option("--ref-id", type=int, help="An integer ID for a reference curve", required=True)
@click.option("--alg", type=str, help="Algorithm name", required=True)
@click.option("--metric-filter", type=click.Choice(MetricFilter), default=MetricFilter.All)  # type: ignore
def measure(ref_id=int, alg=str, metric_filter=MetricFilter):
    """Note a measure"""
    logger.info(f"calculating note with metric type {metric_filter}")
    measure_mark = upsert_mark(prod_db_session, alg, ref_id, metric_filter)
    logger.info(f"Note for measure is: {measure_mark}")
