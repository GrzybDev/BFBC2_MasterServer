from pydantic import Field, IPvAnyAddress

from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class QueueEnteredRequest(TheaterTransaction):
    R_INT_IP: IPvAnyAddress = Field(alias="R-INT-IP")
    R_INT_PORT: int = Field(alias="R-INT-PORT")
    NAME: str
    PID: int
    UID: int
    LID: int
    GID: int


class QueueEnteredResponse(TheaterTransaction):
    pass
