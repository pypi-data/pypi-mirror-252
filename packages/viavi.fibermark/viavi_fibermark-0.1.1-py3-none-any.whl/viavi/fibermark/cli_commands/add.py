from typing import Optional

import click

from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.db_utils.db_insertion import (
    write_measure_to_database,
    write_sor_file_to_database,
)
from viavi.fibermark.db_utils.orm import Algorithm
from viavi.fibermark.notation.algo import upsert_mark_algo
from viavi.fibermark.notation.helpers import MetricFilter


@click.group()
def add():
    """
    Add command group. (Adds Ref/Measure to DB from local files)
    """
    pass


@add.command()
@click.option("--ref-id", type=int, help="An integer ID")
@click.option(
    "--file-path",
    type=click.Path(exists=True),
    help='File path of the form "foo.sor", please input either ip of file_path',
    required=True,
)
@click.option(
    "--category",
    type=str,
    help="category column of the reference Table for easy filtering of data",
)
def reference(
    ref_id: Optional[int],
    file_path: str,
    category: str,
):
    """
    Add a reference curve, if --ref-id is specified, upsert the reference if a reference
    with this id already exists either from the .sor file at `file_path`.
    (If it detects that this file already exist in the db i.e: same md5, does not do anything)
    """
    if category is None:
        raise RuntimeError("Please specify category to insert reference")
    write_sor_file_to_database(
        prod_db_session, sor_filepath=file_path, ref_id=ref_id, category=category, insert_sor_data=True
    )
    # Updating algorithm_mark table on adding a new reference, this will update indexes_curves_not_measured_by_alg
    algos = prod_db_session.query(Algorithm).all()
    for algo in algos:
        for metric_filter in MetricFilter:
            upsert_mark_algo(prod_db_session, alg=algo.name, metric_filter=metric_filter)


@add.command()
@click.option("--ref-id", type=int, help="An integer ID", required=True)
@click.option("--file-path", type=click.Path(exists=True), help='File path of the form "foo.sor"', required=True)
@click.option("--alg", type=str, required=True)
def measure(ref_id: int, file_path: str, alg: str):
    """
    Add measure of alg --alg, who will be noted by comparing to reference `--ref-id` from a local filepath
    """
    algorithm_name = write_measure_to_database(prod_db_session, sor_filepath=file_path, ref_id=ref_id, fo_version=alg)
    # Updating algorithm_mark table on adding a new reference
    for metric_filter in MetricFilter:
        upsert_mark_algo(prod_db_session, alg=algorithm_name, metric_filter=metric_filter)
