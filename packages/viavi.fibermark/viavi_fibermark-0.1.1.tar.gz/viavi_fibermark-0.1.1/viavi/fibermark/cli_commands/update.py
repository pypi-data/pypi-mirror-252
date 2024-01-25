import click

from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.db_utils.db_insertion import upsert_mark
from viavi.fibermark.db_utils.orm import Algorithm
from viavi.fibermark.notation.algo import upsert_mark_algo
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.utils.logging import logger


@click.group()
def update():
    """
    Update command group.
    """
    pass


@update.command()
def marks():
    """Update all mark measures/algo marks"""
    # Your mark logic here
    logger.info("Updating all marks (useful in a change in classifier calculations)")

    algorithms = prod_db_session.query(Algorithm).all()
    for algorithm in algorithms:
        for metric_filter in MetricFilter:
            for measure in algorithm.measures:
                upsert_mark(prod_db_session, algorithm.name, measure.reference_id, metric_filter)
            upsert_mark_algo(prod_db_session, algorithm.name, metric_filter)
        logger.info(f"Finished re marking {algorithm.name}")
