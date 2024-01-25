import json
from dataclasses import field
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class FilterOptions:
    pulse_ns: list[int]
    eval_category: list[str]
    files_to_skip: list[int]
    eval_only_file: list[int] = field(default_factory=list)  # If not empty, eval only files in list
    file_extension: Optional[str] = None

    def __post_init__(self):
        assert self.file_extension in [
            None,
            ".sor",
            ".msor",
        ], f"Filtering {self.file_extension} files, we do not have them in db, or update me ?"


def load_filters_from_json(file_path: str) -> FilterOptions:
    with open(file_path) as json_file:
        data = json.load(json_file)
    return FilterOptions(**data)
