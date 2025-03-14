from typing import Optional

from pydantic import Field

from bfbc2_masterserver.enumerators.theater.JoinMode import JoinMode
from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class UpdateGameRequest(TheaterTransaction):
    class Config:
        extra = "forbid"

    LID: int
    GID: int

    name: Optional[str] = Field(alias="NAME", default=None)
    serverEA: Optional[bool] = Field(alias="B-U-EA", default=None)
    providerId: Optional[str] = Field(alias="B-U-Provider", default=None)
    queueLength: Optional[int] = Field(alias="B-U-QueueLength", default=None)
    serverSoftcore: Optional[bool] = Field(alias="B-U-Softcore", default=None)
    gameTime: Optional[str] = Field(alias="B-U-Time", default=None)
    gameElo: Optional[int] = Field(alias="B-U-elo", default=None)
    gameMod: Optional[str] = Field(alias="B-U-gameMod", default=None)
    gameMode: Optional[str] = Field(alias="B-U-gamemode", default=None)
    gameHash: Optional[str] = Field(alias="B-U-hash", default=None)
    gameLevel: Optional[str] = Field(alias="B-U-level", default=None)
    gamePublic: Optional[bool] = Field(alias="B-U-public", default=None)
    gameRegion: Optional[str] = Field(alias="B-U-region", default=None)
    gameSGUID: Optional[int] = Field(alias="B-U-sguid", default=None)
    joinMode: Optional[JoinMode] = Field(alias="JOIN", default=None)
    maxPlayers: Optional[int] = Field(alias="MAX-PLAYERS", default=None)
    numObservers: Optional[int] = Field(alias="B-numObservers", default=None)
    maxObservers: Optional[int] = Field(alias="B-maxObservers", default=None)


class UpdateGameResponse(TheaterTransaction):
    pass
