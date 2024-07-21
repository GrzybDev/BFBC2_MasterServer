import re
from typing import Optional

from pydantic import Field

from bfbc2_masterserver.messages.theater.TheaterMessage import TheaterMessage


class UpdateGameDetailsRequest(TheaterMessage):
    class Config:
        extra = "allow"

    LID: int
    GID: int


class UpdateGameDetailsResponse(TheaterMessage):
    pass
