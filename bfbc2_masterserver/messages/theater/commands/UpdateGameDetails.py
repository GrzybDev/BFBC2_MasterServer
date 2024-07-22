import re
from typing import Optional

from pydantic import Field

from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class UpdateGameDetailsRequest(TheaterTransaction):
    class Config:
        extra = "allow"

    LID: int
    GID: int


class UpdateGameDetailsResponse(TheaterTransaction):
    pass
