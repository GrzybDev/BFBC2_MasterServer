from pydantic import Field

from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class GetLobbyListRequest(TheaterTransaction):
    FILTER_FAV_ONLY: bool = Field(alias="FILTER-FAV-ONLY")
    FILTER_NOT_FULL: bool = Field(alias="FILTER-NOT-FULL")
    FILTER_NOT_PRIVATE: bool = Field(alias="FILTER-NOT-PRIVATE")
    FILTER_NOT_CLOSED: bool = Field(alias="FILTER-NOT-CLOSED")
    FILTER_MIN_SIZE: int = Field(alias="FILTER-MIN-SIZE")
    FAV_PLAYER: str = Field(alias="FAV-PLAYER")
    FAV_GAME: str = Field(alias="FAV-GAME")
    FAV_PLAYER_UID: str = Field(alias="FAV-PLAYER-UID")


class GetLobbyListResponse(TheaterTransaction):
    NUM_LOBBIES: int = Field(alias="NUM-LOBBIES")


class LobbyData(TheaterTransaction):
    LID: int
    PASSING: int
    NAME: str
    LOCALE: str
    MAX_GAMES: int = Field(alias="MAX-GAMES")
    NUM_GAMES: int = Field(alias="NUM-GAMES")

    # Seems to be static in the original server
    FAVOURITE_GAMES: int = Field(alias="FAVOURITE-GAMES", default=0)
    FAVOURITE_PLAYERS: int = Field(alias="FAVOURITE-PLAYERS", default=0)
