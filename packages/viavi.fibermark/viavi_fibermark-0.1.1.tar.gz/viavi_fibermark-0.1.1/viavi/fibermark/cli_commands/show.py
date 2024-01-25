from typing import Optional

import click
from sqlalchemy.exc import SQLAlchemyError

from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.db_utils.orm import Algorithm, Mark, Reference
from viavi.fibermark.db_utils.query_helpers import select_algo_mark, select_measure
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.utils.helpers import batch_query_result_to_printable_data
from viavi.fibermark.utils.logging import logger, pretty_print


@click.group()
def show():
    """
    Show command group.
    """
    pass


@show.command()
def algo():
    """Output a tabular format of all info on algo and their overall notes on DB"""
    logger.info("Showing algorithm information and mark in tabular format...\n")
    try:
        algorithms = prod_db_session.query(Algorithm).all()
        # Create a list of dictionaries to store the data
        algorithm_data = batch_query_result_to_printable_data(algorithms)

        pretty_print(algorithm_data)

    except SQLAlchemyError as e:
        print(f"Error fetching data from Algorithm table: {e}")


@click.option("--ref-id", type=int, help="An integer ID")
@show.command()
def reference(ref_id: Optional[int]):
    """Outputs a tabular format of all info on curves"""
    logger.info("Showing reference curve information in tabular format...\n")
    try:
        if ref_id is None:
            logger.warning("No id has been specified, showing all reference curves\n")
            references = prod_db_session.query(Reference).all()
        else:
            references = prod_db_session.query(Reference).filter(Reference.id == ref_id).all()
            if len(references) == 0:
                logger.error(f"No reference curve with this id: {id} has been found")

        # Create a list of dictionaries to store the data
        reference_data = batch_query_result_to_printable_data(references)
        # Use tabulate to pretty print the data
        pretty_print(reference_data)
    except SQLAlchemyError as e:
        print(f"Error fetching data from Reference table: {e}")


@show.command()
@click.option("--ref-id", type=int, help="An integer ID", required=True)
@click.option("--alg", type=str, help="Algorithm name", required=True)
def measure(ref_id: int, alg: int):
    """Output a tabular format of info for a measure on a curve identified by ref-id of a given algorithm"""
    logger.info(
        f"Showing measure information for algorithm {alg} and curve reference whose id is {ref_id} in tabular"
        " format...\n"
    )
    measures = select_measure(prod_db_session, ref_id, alg)
    # Convert the Measure objects to dictionaries
    measure_data = batch_query_result_to_printable_data([measures])
    # Use tabulate to pretty print the data
    pretty_print(measure_data)


@show.command()
@click.option("--ref-id", type=int, help="An integer ID who point to a reference curve in DB", required=True)
@click.option("--alg", type=str, help="Algorithm name", required=True)
def mark(ref_id: Optional[int], alg: str):
    """Show mark of an algorithm on given curve"""
    meas = select_measure(prod_db_session, ref_id, alg)
    marks: list[Mark] = meas.marks
    marks_data = batch_query_result_to_printable_data(marks)
    pretty_print(marks_data)


@show.command()
@click.option("--alg", type=str, help="Algorithm name", required=True)
@click.option("--metric-filter", type=click.Choice(MetricFilter), default=MetricFilter.All)  # type: ignore
def algo_mark(alg: int, metric_filter: MetricFilter):
    """Show mark of an algorithm on all curve"""
    alg_mark = select_algo_mark(prod_db_session, alg, metric_filter)
    alg_mark_data = batch_query_result_to_printable_data([alg_mark])
    pretty_print(alg_mark_data)
