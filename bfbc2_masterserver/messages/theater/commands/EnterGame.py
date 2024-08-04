from typing import Optional

from pydantic import Field, IPvAnyAddress

from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class EnterGameRequest(TheaterTransaction):
    PORT: int
    R_INT_PORT: int = Field(alias="R-INT-PORT")
    R_INT_IP: IPvAnyAddress = Field(alias="R-INT-IP")
    PTYPE: str
    LID: int
    GID: int


class EnterGameResponse(TheaterTransaction):
    LID: int
    GID: int

    QPOS: Optional[int] = None
    QLEN: Optional[int] = None


class EnterGameHostRequest(TheaterTransaction):
    R_INT_IP: IPvAnyAddress = Field(alias="R-INT-IP")
    R_INT_PORT: int = Field(alias="R-INT-PORT")
    IP: IPvAnyAddress
    PORT: int
    NAME: str
    PTYPE: str
    TICKET: str
    PID: int
    UID: int
    LID: int
    GID: int


class EnterGameNotice(TheaterTransaction):
    PL: int
    TICKET: str
    PID: int
    I: IPvAnyAddress
    P: int
    HUID: int
    INT_PORT: int = Field(alias="INT-PORT")
    EKEY: str
    INT_IP: IPvAnyAddress = Field(alias="INT-IP")
    UGID: str
    LID: int
    GID: int
