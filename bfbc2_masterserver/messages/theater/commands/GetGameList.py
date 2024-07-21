from typing import Optional

from pydantic import Field, IPvAnyAddress

from bfbc2_masterserver.messages.theater.TheaterMessage import TheaterMessage


class GetGameListRequest(TheaterMessage):
    LID: int
    GID: Optional[int] = None
    TYPE: str
    FILTER_FAV_ONLY: bool = Field(alias="FILTER-FAV-ONLY")
    FILTER_NOT_FULL: bool = Field(alias="FILTER-NOT-FULL")
    FILTER_NOT_PRIVATE: bool = Field(alias="FILTER-NOT-PRIVATE")
    FILTER_NOT_CLOSED: bool = Field(alias="FILTER-NOT-CLOSED")
    FILTER_MIN_SIZE: int = Field(alias="FILTER-MIN-SIZE")
    FILTER_ATTR_U_gameMod: str = Field(alias="FILTER-ATTR-U-gameMod")
    FAV_PLAYER: str = Field(alias="FAV-PLAYER")
    FAV_GAME: str = Field(alias="FAV-GAME")
    COUNT: int
    FAV_PLAYER_UID: str = Field(alias="FAV-PLAYER-UID")
    FAV_GAME_UID: str = Field(alias="FAV-GAME-UID")


class GetGameListResponse(TheaterMessage):
    LOBBY_NUM_GAMES: int = Field(alias="LOBBY-NUM-GAMES")
    NUM_GAMES: int = Field(alias="NUM-GAMES")
    LID: int
    LOBBY_MAX_GAMES: int = Field(alias="LOBBY-MAX-GAMES")


class GameData(TheaterMessage):
    LID: int
    GID: int
    N: str
    AP: int
    JP: int
    QP: int
    MP: int
    F: int
    NF: int
    HU: int
    HN: str
    I: IPvAnyAddress
    P: int
    J: str
    PL: str
    PW: int
    V: str
    TYPE: str
    B_numObservers: int = Field(alias="B-numObservers")
    B_maxObservers: int = Field(alias="B-maxObservers")
    B_version: str = Field(alias="B-version")
    B_U_region: str = Field(alias="B-U-region")
    B_U_level: str = Field(alias="B-U-level")
    B_U_elo: int = Field(alias="B-U-elo")
    B_U_Softcore: int = Field(alias="B-U-Softcore")
    B_U_Hardcore: int = Field(alias="B-U-Hardcore")
    B_U_EA: int = Field(alias="B-U-EA")
    B_U_HasPassword: int = Field(alias="B-U-HasPassword")
    B_U_public: int = Field(alias="B-U-public")
    B_U_QueueLength: int = Field(alias="B-U-QueueLength")
    B_U_gameMod: str = Field(alias="B-U-gameMod")
    B_U_gamemode: str = Field(alias="B-U-gamemode")
    B_U_sguid: int = Field(alias="B-U-sguid")
    B_U_Provider: str = Field(alias="B-U-Provider")
    B_U_Time: str = Field(alias="B-U-Time")
    B_U_hash: str = Field(alias="B-U-hash")
    B_U_Punkbuster: int = Field(alias="B-U-Punkbuster")
    B_U_PunkBusterVersion: Optional[str] = Field(alias="B-U-PunkBusterVersion")
