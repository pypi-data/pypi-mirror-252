from dataclasses import astuple, dataclass
from pathlib import Path
from typing import Any, Optional

from sqlalchemy import not_
from sqlalchemy.orm import Query, Session
from type_checker.decorators import enforce_strict_types

from viavi.fibermark.cli_commands.filtering_helpers import FilterOptions
from viavi.fibermark.db_utils.orm import ParsedSorData, Reference

DIR_REF_FILES = "ref_files/"


@enforce_strict_types
@dataclass
class RefFileInfo:
    ref_id: int
    filepath: str

    def __iter__(self):
        return iter(astuple(self))


def enrich_query_filters(query: Query[Any], filter_options: Optional[FilterOptions]) -> Query[Any]:
    if filter_options is not None:
        if filter_options.file_extension is not None:
            query = query.filter(Reference.path.like(f"%{filter_options.file_extension}%"))
        if len(filter_options.eval_only_file) != 0:
            query = query.filter(Reference.id.in_(filter_options.eval_only_file))
            return query
        if len(filter_options.eval_category) != 0:
            query = query.filter(Reference.category.in_(filter_options.eval_category))
        if len(filter_options.pulse_ns) != 0:
            query = query.filter(Reference.pulse_ns.in_(filter_options.pulse_ns))
        query = query.filter(not_(Reference.id.in_(filter_options.files_to_skip)))
    return query


def get_all_ref_files(session: Session, filter_options: Optional[FilterOptions] = None) -> list[RefFileInfo]:
    """_summary_ This function should always be used to retrieve ref files for any purposes.

    Args:
        session (Session): _description_
        ftp_host (FTPHost): _description_
        filter_options: Optional[FilterOptions]: Filtering ref files we want to check
    Returns:
        list[RefFileInfo]: Go search all file infos from Prof DB
    """
    ref_files_query = session.query(Reference.id, Reference.path, ParsedSorData.binary_dump).join(ParsedSorData)
    ref_files_query = enrich_query_filters(ref_files_query, filter_options)
    Path(DIR_REF_FILES).mkdir(exist_ok=True)
    ref_files_locally_stored = []
    for ref_id, file_path, binary_dump_sor_file in ref_files_query.all():
        ref_file_local_storage = DIR_REF_FILES + Path(file_path).name
        with Path(ref_file_local_storage).open(mode="wb") as locally_stored_file:
            locally_stored_file.write(binary_dump_sor_file)
        ref_files_locally_stored.append(RefFileInfo(ref_id, ref_file_local_storage))
    return ref_files_locally_stored


@enforce_strict_types
@dataclass
class FOEval:
    fo_version: str
    list_new_measures_to_write_to_db: list[RefFileInfo]
    set_failed_measures_ref_id: set[int]

    def __iter__(self):
        return iter(astuple(self))
