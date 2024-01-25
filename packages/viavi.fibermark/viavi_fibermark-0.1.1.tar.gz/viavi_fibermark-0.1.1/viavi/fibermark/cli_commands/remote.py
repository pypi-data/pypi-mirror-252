import os
from typing import Optional

import click

from viavi.fibermark.cli_commands.filtering_helpers import load_filters_from_json
from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.db_utils.db_insertion import (
    write_measure_to_database,
    write_sor_file_to_database,
)
from viavi.fibermark.db_utils.orm import Algorithm
from viavi.fibermark.notation.algo import upsert_mark_algo
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.utils.logging import logger
from viavi.fibermark.utils.platform_helpers import (
    ask_fo_eval_and_write_measures_to_db,
    connect_platform,
    retrieve_current_curve_locally,
    retrieve_fo_version,
)


@click.group()
def remote():
    """
    Remote command group. (Upserts to DB from remote)
    """
    pass


@remote.command()
@click.option("--ref-id", type=int, help="An integer ID")
@click.option(
    "--ip",
    type=str,
    help='IP address of a base like "10.33.17.123", please input either ip of file_path',
    required=True,
)
@click.option("--user", type=str, help="ftp_user to connect to IP", required=True)
@click.option("--passwd", type=str, help="ftp_passwd to connect to IP", required=True)
@click.option(
    "--category",
    type=str,
    help="category column of the reference Table for easy filtering of data",
)
def reference(
    ref_id: Optional[int],
    ip: str,
    user: str,
    passwd: str,
    category: Optional[str],
):
    """
    Add a reference curve, if --ref-id is specified, upsert the reference
    either from the file_path (using local state of the file) or from a base whose IP is inputted
    (if ip inputted, needs user and password for base)
    (replace if it exists already and iff no file with this md5 exist in DB)
    """
    if category is None:
        category = "Non-Regression"
        logger.info(f"Defaulting to category {category} because none was inputted")
    file_path = retrieve_current_curve_locally(ip, ftp_user=user, ftp_passwd=passwd, make_measure=False)
    assert os.path.isfile(file_path)
    write_sor_file_to_database(
        prod_db_session, sor_filepath=file_path, ref_id=ref_id, category=category, insert_sor_data=True
    )
    # Updating algorithm_mark table on adding a new reference
    algos = prod_db_session.query(Algorithm).all()
    for algo in algos:
        for metric_filter in MetricFilter:
            upsert_mark_algo(prod_db_session, alg=algo.name, metric_filter=metric_filter)


@remote.command()
@click.option("--ref-id", type=int, help="An integer ID", required=True)
@click.option(
    "--ip",
    type=str,
    help='IP address of a base like "10.33.17.123", please input either ip of file_path',
    required=True,
)
@click.option("--user", type=str, help="ftp_user to connect to IP", required=True)
@click.option("--passwd", type=str, help="ftp_passwd to connect to IP", required=True)
def measure(ref_id: int, ip: str, user: str, passwd: str):
    """
    Add measure, who will be noted by comparing to reference `--ref-id` from an ip address
    """
    logger.info(
        f"ip '{ip}' has been specified, user is {user}, password is {passwd} retrieving file and making measure"
    )
    file_path = retrieve_current_curve_locally(ip, ftp_user=user, ftp_passwd=passwd, make_measure=True)
    assert os.path.isfile(file_path)
    mts = connect_platform(ip)
    fo_version = retrieve_fo_version(mts)
    algorithm_name = write_measure_to_database(prod_db_session, file_path, ref_id, fo_version)
    # Updating algorithm_mark table on adding a new reference
    for metric_filter in MetricFilter:
        upsert_mark_algo(prod_db_session, alg=algorithm_name, metric_filter=metric_filter)


@remote.command()
@click.option(
    "--ip",
    type=str,
    help='IP address of a base like "10.33.17.123", please input either ip of file_path',
    required=True,
)
@click.option("--user", type=str, help="ftp_user to connect to IP", required=True)
@click.option("--passwd", type=str, help="ftp_passwd to connect to IP", required=True)
@click.option(
    "--debug",
    is_flag=True,
    help="Keep all files and measured files on base",
)
@click.option(
    "--unofficial_fo_name",
    type=str,
    help=(
        "If this parameter is specified, fo_version in DB will have specified name.\n Please use this to eval"
        " unofficial FO versions when you want to test your changes"
    ),
)
@click.option("--use_filters", type=click.Path(exists=True))
def eval_fo(
    ip: str, user: str, passwd: str, debug: bool, unofficial_fo_name: Optional[str], use_filters: Optional[str]
):
    """
    Evaluates FO, from all curves in reference of connected DB
    """
    if use_filters is not None:
        filter_options = load_filters_from_json(use_filters)
    else:
        filter_options = None
    fo_eval, measures_failed_to_write_to_db = ask_fo_eval_and_write_measures_to_db(
        prod_db_session, ip, user, passwd, debug, filter_options, unofficial_fo_name
    )
    failed_measures = fo_eval.set_failed_measures_ref_id
    if len(failed_measures) > 0:
        logger.warning(f"Could not measure all files from ref db, files not measured are {failed_measures}")
    if len(measures_failed_to_write_to_db) > 0:
        logger.fatal(f"Could not write to db sucessfully measured curves: {measures_failed_to_write_to_db}")
