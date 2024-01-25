from os import listdir
from os.path import isfile, join
from pathlib import Path

from sqlalchemy.orm import Session

from viavi.fibermark.db_utils.connect import prod_db_session
from viavi.fibermark.db_utils.db_insertion import write_sor_file_to_database
from viavi.fibermark.notation.algo import upsert_mark_algo
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.utils.logging import logger


def write_directory_sor_files_to_database(session: Session, sor_filepath_directory: str, category: str):
    list_files_directory = [
        sor_filepath_directory + file
        for file in listdir(sor_filepath_directory)
        if isfile(join(sor_filepath_directory, file))
    ]
    filenames_failed = []
    for file in list_files_directory:
        try:
            write_sor_file_to_database(session, file, ref_id=None, category=category, insert_sor_data=True)
        except Exception as e:
            logger.fatal(f"Failure due to {e}")
            filenames_failed.append(Path(file).name)
    logger.warning(
        f"Failed to insert {len(filenames_failed)} files due to bad file extension (.msor)/parsing fail or file already"
        f" here which are : \n {filenames_failed}"
    )
    for metric_filter in MetricFilter:
        result_algo_mark = upsert_mark_algo(prod_db_session, "reference", metric_filter)


if __name__ == "__main__":
    directory_to_import = "/home/aboussejra/inspect/courbes_prof_production_V2/"
    write_directory_sor_files_to_database(prod_db_session, directory_to_import, "TEMP")
