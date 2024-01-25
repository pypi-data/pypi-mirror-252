import os
import re
import socket
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from aenum import Enum
from ftputil import FTPHost
from sqlalchemy.orm import Session
from type_checker.decorators import enforce_strict_types
from viavi.placopy.instrument.viavi_base.mts import MTS

from viavi.fibermark.cli_commands.filtering_helpers import FilterOptions
from viavi.fibermark.db_utils.db_insertion import write_measure_to_database
from viavi.fibermark.notation.algo import upsert_mark_algo
from viavi.fibermark.notation.helpers import MetricFilter
from viavi.fibermark.utils.fo_eval_helpers import FOEval, RefFileInfo, get_all_ref_files
from viavi.fibermark.utils.ftp_helpers import ftp_connect
from viavi.fibermark.utils.logging import logger

PLACE_FIBER_MARK_TEMP_FILES = "disk/fiber_mark_temp/"
DIR_LOCAL_TRANSFERRED_FILES = "temp/"


@enforce_strict_types
@dataclass
class ConnectionSetup:
    ftp_host: FTPHost
    mts: MTS
    ftp_working_path: str
    fo_version: str


class Platform(Enum):
    # Add others when needed
    MTS1000 = "MTS1000"
    x86 = "x86"


def ping_base(server: str, port: int, timeout=3):
    """ping server"""
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
    except OSError:
        return False
    else:
        s.close()
        return True


def connect_platform(ip: str) -> MTS:
    """Trying to connect for telnet on ip at port 8002 or 8003 as it depends on platforms"""
    if ping_base(ip, 8002):
        logger.info(f"Server can be pinged at port {8002}, trying to connect")
        mts = MTS(ip)
    elif ping_base(ip, 8003):
        logger.info(f"Server can be pinged at port {8003}, trying to connect")
        mts = MTS(ip)
    else:
        raise RuntimeError("Cannot connect to IP")
    logger.info(f"Platform is {mts.base_type}")
    return mts


def find_where_disk_is_located(mts: MTS) -> str:
    """_summary_
    Args:
        mts (MTS): _description_

    Returns:
        fisk_location (str): location of disk on base (can be /acterna/user/disk or /user/disk)
    """
    if mts.base_type == Platform.MTS1000.name:  # type: ignore
        disk_location = "/"
    else:
        disk_location = "/acterna/"
    return disk_location + "user/"


def retrieve_fo_version(mts: MTS) -> str:
    """

    Args:
        mts (MTS): PlaCoPy object from MTS

    Returns:
        fo_version: string of pattern like FO: 22.64
    """
    fo_version: str = mts.fo.foversion.get()
    match = re.search("\d{2}.\d{2}", fo_version)
    if match:
        ver_number = match.group()
    version = f"FO: {ver_number}"
    logger.info(f"Platform is on version {version}")
    return version


@enforce_strict_types
def remote_connection_routine(ip: str, ftp_user: str, ftp_passwd: str) -> ConnectionSetup:
    mts = connect_platform(ip)
    fo_version = retrieve_fo_version(mts)
    ftth_slm_licence_status = mts.fo.status.licence.get('"FTTH_SLM"')
    if ftth_slm_licence_status != "VALID":
        raise RuntimeError(f"I do not have licence FTTH_SLM, Status is {ftth_slm_licence_status} Measure could differ on msors file. Stopping run")
    ftp_host = ftp_connect(ip, ftp_user, ftp_passwd)
    remote_disk_location = find_where_disk_is_located(mts)
    ftp_working_path = remote_disk_location + PLACE_FIBER_MARK_TEMP_FILES
    logger.info(f"Registering files on remote at {ftp_working_path}, directory will be cleaned later")
    fo_working_path: str = PLACE_FIBER_MARK_TEMP_FILES
    try:
        ftp_host.makedirs(ftp_working_path)
    except Exception:
        RuntimeError(f"Failed at making temp directory in {remote_disk_location}")
    # Making FO work dir the newly created dir
    try:
        logger.debug(f"File for FO will be stored at {fo_working_path}")
        mts.fo.fsetup.wpath.set(f'"{fo_working_path}"')
        mts.fo.fsetup.dirname.set('"[Current_Dir]"')
        ftp_host.chdir(ftp_working_path)
    except Exception as e:
        logger.fatal(f"Could not move to {fo_working_path} due to {e}")
        ftp_host.chdir("../")
        ftp_host.rmdir(ftp_working_path)
        RuntimeError(f"Could not go to {PLACE_FIBER_MARK_TEMP_FILES} directory")
    return ConnectionSetup(ftp_host, mts, ftp_working_path, fo_version)


@enforce_strict_types
def cleanup_transfer_artifacts(mts: MTS, ftp_host: FTPHost, ftp_working_path: str) -> None:
    logger.debug("Cleanup up created files and folders")
    # Going back to old dir
    mts.fo.fsetup.wpath.set('"disk/"')
    try:
        for file in ftp_host.listdir(ftp_host.getcwd()):
            ftp_host.remove(file)
        ftp_host.chdir("../")
        ftp_host.rmdir(ftp_working_path)
    except Exception as e:
        raise Exception(f"Problem in cleaning up created directories/files by ftp\n{e}")


@enforce_strict_types
def file_storage_and_transfer(
    mts: MTS,
    ftp_host: FTPHost,
    ftp_working_path: str,
    make_measure: bool,
    local_addition_to_filename: Optional[str] = None,
) -> str:
    files_before_writing = [file for file in ftp_host.listdir(ftp_working_path) if ftp_host.path.isfile(file)]
    if make_measure:
        # Refreshing Mes auto
        mes_auto_command = mts.fo.otdresult.mauto.get()
        if mes_auto_command != "OK":
            raise Exception(f"Could not make measure on host {mts.ip}")
    # Storing file with its filename
    logger.debug(f"Before writing, we have files : {files_before_writing}")
    storing_command = mts.fo.file.store.get()
    if storing_command != "OK":
        raise Exception(f"Could not store loaded file on {mts.ip}")
    files_after_writing = [file for file in ftp_host.listdir(ftp_working_path) if ftp_host.path.isfile(file)]
    logger.debug(f"After writing, we have files : {files_after_writing}")
    new_files = list(set(files_after_writing) - set(files_before_writing))
    if len(new_files) == 0:
        ftp_host.chdir("../")
        ftp_host.rmdir(ftp_working_path)
        raise RuntimeError("Could not find newly stored file")
    new_file: str = new_files[0]
    logger.info(f"Most recent file is {new_file}, downloading...")
    Path(DIR_LOCAL_TRANSFERRED_FILES).mkdir(exist_ok=True)
    local_filepath = DIR_LOCAL_TRANSFERRED_FILES + new_file
    if local_addition_to_filename is not None:
        base_filename, file_extension = os.path.splitext(local_filepath)
        local_filepath = base_filename + local_addition_to_filename + file_extension
    ftp_host.download(new_file, local_filepath)
    return local_filepath


@enforce_strict_types
def retrieve_current_curve_locally(
    ip: str,
    ftp_user: str,
    ftp_passwd: str,
    make_measure: bool = False,
    local_addition_to_filename: Optional[str] = None,
) -> str:
    connection_setup = remote_connection_routine(ip, ftp_user, ftp_passwd)
    ftp_host = connection_setup.ftp_host
    mts = connection_setup.mts
    ftp_working_path = connection_setup.ftp_working_path
    locally_stored_filepath = file_storage_and_transfer(
        mts, ftp_host, ftp_working_path, make_measure, local_addition_to_filename
    )
    try:
        cleanup_transfer_artifacts(mts, ftp_host, ftp_working_path)
    except Exception:
        logger.warning(f"Could not cleanup transfer artifacts at {ftp_working_path}, please cleanup by yourself :(")
    return locally_stored_filepath


@enforce_strict_types
def send_files_remote(list_local_ref_files: list[RefFileInfo], connection_setup: ConnectionSetup) -> list[RefFileInfo]:
    list_remote_filepaths = []
    # Creating temp folder for measured files if not exist
    Path(DIR_LOCAL_TRANSFERRED_FILES).mkdir(exist_ok=True)
    # Upload to host ref files
    for ref_id, ref_local_filepath in list_local_ref_files:
        filename = Path(ref_local_filepath).name
        base_remote_filepath = connection_setup.ftp_working_path + filename
        connection_setup.ftp_host.upload_if_newer(ref_local_filepath, base_remote_filepath)
        list_remote_filepaths.append(RefFileInfo(ref_id, base_remote_filepath))
    return list_remote_filepaths


@enforce_strict_types
def make_measures_and_retrieve_files_locally(
    list_remote_filepaths: list[RefFileInfo], connection_setup: ConnectionSetup
) -> list[RefFileInfo]:
    # Making measure and retrieving files
    list_measures_to_write_to_db = []
    mts = connection_setup.mts
    number_of_files_to_evaluate = len(list_remote_filepaths)
    file_count_evaluation = 1
    temp_dir_name = "fiber_mark_temp"
    for ref_id, base_remote_filepath in list_remote_filepaths:
        logger.info(
            f"Making measure on ref_id {ref_id}, {base_remote_filepath} file"
            f" {file_count_evaluation}/{number_of_files_to_evaluate}"
        )
        file_count_evaluation += 1
        filename = Path(base_remote_filepath).name
        filename_without_extension = Path(base_remote_filepath).stem
        filename_extension = Path(base_remote_filepath).suffix
        logger.debug(f"Loading {filename}")
        loading_scpi_order = f'"{PLACE_FIBER_MARK_TEMP_FILES}","{filename}",CONFIG'
        loading_command = mts.fo.file.load.get(f"{loading_scpi_order}")
        if loading_command != "OK":
            logger.fatal(f"Could not load file {filename}")
            continue
        logger.debug(f"Measuring {filename}")
        mes_auto_command = mts.fo.otdresult.mauto.get()
        if mes_auto_command != "OK":
            logger.fatal(f"Could not make measure on {filename}")
            continue
        # Storing file # FO SCPI order needs filename without extension
        measured_filename_without_extension = f"measured_{filename_without_extension}"
        measured_filename_with_extension = measured_filename_without_extension + filename_extension
        # File naming advanced parameter is used in .csor for file generation
        mts.fo.fsetup.fnaming.set(f'"{measured_filename_without_extension}"')
        if filename_extension == ".sor":
            mts.fo.fsetup.fcmultitrace.set("NO")
            assert mts.fo.fsetup.fcmultitrace.get() == "NO", "Could not set multitrace to NO for .sor file"
        # A directory might be specified in the storing setup and mess with everything.
        # We force this parameter to be on fiber_mark_temp
        mts.fo.fsetup.dirname.set(f'"{temp_dir_name}"')
        assert mts.fo.fsetup.dirname.get() == f'"{temp_dir_name}"', f"Could not set working dir to {temp_dir_name}"
        storing_command = mts.fo.file.store.get(f'"{measured_filename_without_extension}"')
        logger.debug(f"Storing measured {filename}")
        if storing_command != "OK":
            logger.fatal(f"Could not store {measured_filename_with_extension}")
            continue
        # Downloading file with FO measure
        local_path_measured_file = DIR_LOCAL_TRANSFERRED_FILES + measured_filename_with_extension
        # SCPI COMMAND is inconsistent, on .csor file it may fail storing file while sending back OK
        try:
            connection_setup.ftp_host.download(
                connection_setup.ftp_working_path + measured_filename_with_extension, local_path_measured_file
            )
        except Exception:
            logger.fatal(f"Could not get back measure_{filename}")
            continue
        list_measures_to_write_to_db.append(RefFileInfo(ref_id, local_path_measured_file))
    return list_measures_to_write_to_db


@enforce_strict_types
def write_measures_to_db_and_note_algo(
    session: Session, fo_version: str, list_measures_to_write_to_db: list[RefFileInfo]
) -> list[str]:
    # Writing retrieved measures to DB
    algorithms_measures = []
    measures_failed_to_write_to_db = []
    for ref_id, local_path_measured_file in list_measures_to_write_to_db:
        try:
            algorithm_name = write_measure_to_database(session, local_path_measured_file, ref_id, fo_version)
            algorithms_measures.append(algorithm_name)
        except Exception as e:
            measures_failed_to_write_to_db.append(ref_id)
            logger.fatal(f"Could not add to db measure at {local_path_measured_file} due to error {e}")
    distinct_algorithms_measures: set[str] = set(algorithms_measures)
    distinct_algorithms_count = len(distinct_algorithms_measures)
    if distinct_algorithms_count > 1:
        logger.fatal(
            f"Found {distinct_algorithms_count} fo_versions which are {distinct_algorithms_measures} on same base,"
            " problem in sor file exploitation"
        )
    else:
        logger.info(f"Measures are from algorithm {distinct_algorithms_measures}, marking algorithm...")
    # Marking algorithm
    for metric_filter in MetricFilter:
        upsert_mark_algo(session, alg=algorithm_name, metric_filter=metric_filter)
    return measures_failed_to_write_to_db


@enforce_strict_types
def ask_fo_eval(
    session: Session,
    ip: str,
    user: str,
    passwd: str,
    debug: bool,
    filter_options: Optional[FilterOptions],
) -> FOEval:
    fo_connection_setup = remote_connection_routine(ip, user, passwd)
    ref_files_locally_stored = get_all_ref_files(session, filter_options)
    list_ref_file_ids = [file.ref_id for file in ref_files_locally_stored]
    set_failed_measures_ref_id: set[int] = set()
    try:
        list_remote_filepaths = send_files_remote(ref_files_locally_stored, fo_connection_setup)
        list_new_measures_to_write_to_db = make_measures_and_retrieve_files_locally(
            list_remote_filepaths, fo_connection_setup
        )
        list_successfully_measured_ref_ids = [file.ref_id for file in list_new_measures_to_write_to_db]
        # Find diff in ref_ids, logger.warning it (maybe not raise error but return if could not measure ?)
        set_failed_measures_ref_id = set(list_ref_file_ids) - set(list_successfully_measured_ref_ids)
    except Exception as e:
        raise Exception(f"Stumbled upon error {e} while evaluating FO")
    finally:
        if debug:
            logger.warning(
                "Debug mode on, keeping all files on remote base, please cleanup manually before relaunching an eval on"
                " this platform"
            )
            pass
        else:
            try:
                cleanup_transfer_artifacts(
                    fo_connection_setup.mts, fo_connection_setup.ftp_host, fo_connection_setup.ftp_working_path
                )
            except Exception:
                logger.warning(
                    f"Could not cleanup transfer artifacts at {fo_connection_setup.ftp_working_path}, please cleanup by"
                    " yourself :("
                )
    return FOEval(fo_connection_setup.fo_version, list_new_measures_to_write_to_db, set_failed_measures_ref_id)


def ask_fo_eval_and_write_measures_to_db(
    session: Session,
    ip: str,
    user: str,
    passwd: str,
    debug: bool,
    filter_options: Optional[FilterOptions],
    unofficial_fo_name: Optional[str],
) -> Tuple[FOEval, list[str]]:
    fo_eval = ask_fo_eval(session, ip, user, passwd, debug, filter_options)
    if unofficial_fo_name is not None:
        fo_eval.fo_version = unofficial_fo_name
        logger.info(f"Evaluation custom specified FO version whose name is {fo_eval.fo_version}")
    measures_failed_to_write_to_db = write_measures_to_db_and_note_algo(
        session, fo_eval.fo_version, fo_eval.list_new_measures_to_write_to_db
    )
    return fo_eval, measures_failed_to_write_to_db
