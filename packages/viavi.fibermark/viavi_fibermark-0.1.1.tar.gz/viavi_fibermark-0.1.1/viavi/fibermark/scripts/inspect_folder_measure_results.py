import fnmatch
import os

from viavi.fiberparse.Data.SORData import MethodeMesure, SORData
from viavi.fiberparse.FileParser.SORParser import SORParser

from viavi.fibermark.utils.fo_eval_helpers import RefFileInfo
from viavi.fibermark.utils.logging import logger
from viavi.fibermark.utils.platform_helpers import (
    make_measures_and_retrieve_files_locally,
    remote_connection_routine,
    send_files_remote,
)


def find_sor_files(folder_path):
    sor_files = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in fnmatch.filter(files, "*.sor"):
            sor_files.append(os.path.join(root, file_name))
    return sor_files


sor_files = find_sor_files("/home/aboussejra/inspect/BT_OR_problematic_data")

fo_connection_setup = remote_connection_routine("localhost", "aboussejra", "users123")
dummy_list_ref_files = [RefFileInfo(i, sor_filepath) for i, sor_filepath in enumerate(sor_files)]
list_remote_filepaths = send_files_remote(dummy_list_ref_files, fo_connection_setup)
list_measures_to_write_to_db = make_measures_and_retrieve_files_locally(list_remote_filepaths, fo_connection_setup)

ml_added_events_all_filenames = {}
count_added_events = 0
for dummy_id_not_meaning_anything, local_measured_filepath in list_measures_to_write_to_db:
    print(f"Locally measured file is in {local_measured_filepath}")
    sor_data: SORData = SORParser().getData(local_measured_filepath)
    ml_added_events_filename = []
    for event in sor_data.events:
        if event.methode_mesure == MethodeMesure.eEvtMethode_ML:
            logger.info(f"Found event {event} by ML in {local_measured_filepath}")
            ml_added_events_filename.append(event)
    count_added_events += len(ml_added_events_filename)
    ml_added_events_all_filenames[local_measured_filepath] = ml_added_events_filename

report_name = f"{count_added_events}_ml_events_{len(list_measures_to_write_to_db)}_files.txt"


for i, (filename, ml_added_events) in enumerate(ml_added_events_all_filenames.items()):
    if len(ml_added_events) != 0:
        logger.info(f"For {filename} {dummy_list_ref_files[i].filepath} we have added: ")
        for ml_added_event in ml_added_events:
            logger.info(f"{ml_added_event}")

logger.warning(f"Added {count_added_events} events to {len(list_measures_to_write_to_db)} files")

# with open(report_name, 'w') as json_file:
#     json.dump(ml_added_events_all_filenames, json_file)

# print(f"Find report at {report_name}")
