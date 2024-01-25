from pathlib import Path
from typing import Union

from viavi.fiberparse.Data.MSORData import MSORData
from viavi.fiberparse.Data.SORData import SORData
from viavi.fiberparse.FileParser.MSORParser import MSORParser
from viavi.fiberparse.FileParser.SORParser import SORParser


def parse_sor_and_derivatives(sor_filepath: str) -> Union[SORData, MSORData]:
    file_extension = Path(sor_filepath).suffix
    if file_extension == ".sor":
        sor_data: SORData = SORParser().getData(sor_filepath)
        return sor_data
    elif file_extension == ".msor":
        msor_data: MSORData = MSORParser().getData(sor_filepath)
        if msor_data.multipulse_events is None:
            raise Exception("Trying to import a MSOR which is not multipulse, currently fibermark does not handle that")
        if len(msor_data.multipulse_events) >= 2:
            raise Exception(
                "Trying to import a MSOR which is multipulse and multilambda, currently fibermark does not handle that"
            )
        return msor_data
    else:
        raise Exception(f"I do not know which parser to select for {file_extension}")
