from typing import Optional

from pydantic import Field

from bfbc2_masterserver.messages.theater.TheaterMessage import TheaterMessage


class UpdateGameRequest(TheaterMessage):
    class Config:
        extra = "allow"

    LID: int
    GID: int


class UpdateGameResponse(TheaterMessage):
    pass
