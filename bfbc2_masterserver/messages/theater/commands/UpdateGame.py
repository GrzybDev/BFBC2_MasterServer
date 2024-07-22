from typing import Optional

from pydantic import Field

from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class UpdateGameRequest(TheaterTransaction):
    class Config:
        extra = "allow"

    LID: int
    GID: int


class UpdateGameResponse(TheaterTransaction):
    pass
