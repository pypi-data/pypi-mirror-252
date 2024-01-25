from pathlib import Path

from viavi.fiberparse.FileParser.MSORParser import MSORParser
from viavi.fiberparse.FileParser.SORParser import SORParser

from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.db_utils.db_insertion import upsert_measure, upsert_parsed_sor_data
from viavi.fibermark.db_utils.orm import Algorithm
from viavi.fibermark.notation.algo import upsert_mark_algo
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.utils.fo_eval_helpers import get_all_ref_files
from viavi.fibermark.utils.logging import logger

ref_files_locally_stored = get_all_ref_files(prod_db_session)
# To update, put all, update Folder in prof remote, then run this script
for ref_id, filepath in ref_files_locally_stored:
    logger.info(f"Writing file {ref_id} out of {len(ref_files_locally_stored)}")
    file_extension = Path(filepath).suffix
    if file_extension == ".csor":
        continue
    elif file_extension == ".sor":
        sor_data = SORParser().getData(filepath)
    elif file_extension == ".msor":
        sor_data = MSORParser().getData(filepath)
    upsert_parsed_sor_data(prod_db_session, Path(filepath), ref_id, sor_data)
    upsert_measure(prod_db_session, "reference", ref_id, sor_data)

algos = prod_db_session.query(Algorithm).all()
for algo in algos:
    for metric_filter in MetricFilter:
        upsert_mark_algo(prod_db_session, alg=algo.name, metric_filter=metric_filter)
    # NEED to remark all algos for algo in algos. Cause reference measure changed.

prod_db_session.commit()
