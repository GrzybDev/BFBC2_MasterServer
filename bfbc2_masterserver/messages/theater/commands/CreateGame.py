from pydantic import Field, IPvAnyAddress, SecretStr

from bfbc2_masterserver.enumerators.theater.GameType import GameType
from bfbc2_masterserver.enumerators.theater.JoinMode import JoinMode
from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class CreateGameRequest(TheaterTransaction):
    LID: int
    RESERVE_HOST: bool = Field(alias="RESERVE-HOST")
    NAME: str
    PORT: int
    HTTYPE: str
    TYPE: GameType
    QLEN: int
    DISABLE_AUTO_DEQUEUE: bool = Field(alias="DISABLE-AUTO-DEQUEUE")
    HXFR: bool
    INT_PORT: int = Field(alias="INT-PORT")
    INT_IP: IPvAnyAddress = Field(alias="INT-IP")
    MAX_PLAYERS: int = Field(alias="MAX-PLAYERS")
    B_maxObservers: int = Field(alias="B-maxObservers")
    B_numObservers: int = Field(alias="B-numObservers")
    UGID: str
    SECRET: SecretStr
    B_U_Hardcore: bool = Field(alias="B-U-Hardcore")
    B_U_HasPassword: bool = Field(alias="B-U-HasPassword")
    B_U_Punkbuster: bool = Field(alias="B-U-Punkbuster")
    B_version: str = Field(alias="B-version")
    JOIN: JoinMode
    RT: str


class CreateGameResponse(TheaterTransaction):
    LID: int
    GID: int
    MAX_PLAYERS: int = Field(alias="MAX-PLAYERS")
    EKEY: str
    UGID: str
    JOIN: str
    SECRET: SecretStr
    J: str
