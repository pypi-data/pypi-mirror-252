from os import listdir
from os.path import isfile, join
from pathlib import Path

import pandas as pd

from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.db_utils.db_insertion import write_sor_file_to_database
from viavi.fibermark.notation.algo import upsert_mark_algo
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.utils.calculate_md5 import md5
from viavi.fibermark.utils.logging import logger

prof_v3_restored_files = "/home/aboussejra/AI/fibermark/Prof_v3_Storage/"

df_state_of_db = pd.read_csv(prof_v3_restored_files + "memory_categories_prof_v2.csv")

list_files_directory = [
    prof_v3_restored_files + file
    for file in listdir(prof_v3_restored_files)
    if isfile(join(prof_v3_restored_files, file))
]
list_files_directory = sorted(list_files_directory)
filenames_failed = []
for file_path in list_files_directory:
    file_id = Path(file_path).stem
    logger.info(f"Looking at {file_id}")
    file_suffix = Path(file_path).suffix
    if "memory_categories_prof_v2" in file_path or "file_not_dumped_from_prof_v2.txt" in file_path:
        continue
    info_file = df_state_of_db[df_state_of_db["id"] == int(file_id)]
    category = info_file["category"].iloc[0]
    assert md5(file_path) == info_file["md5"].iloc[0]
    try:
        write_sor_file_to_database(
            prod_db_session, file_path, ref_id=int(file_id), category=category, insert_sor_data=True
        )
    except Exception as e:
        logger.fatal(f"Failure due to {e}")
        filenames_failed.append(Path(file_path).name)
logger.warning(
    f"Failed to insert {len(filenames_failed)} files due to bad file extension (.msor)/parsing fail or file already"
    f" here which are : \n {filenames_failed}"
)

for metric_filter in MetricFilter:
    result_algo_mark = upsert_mark_algo(prod_db_session, "reference", metric_filter)
