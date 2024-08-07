from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from bfbc2_masterserver.enumerators.client.ClientPlatform import ClientPlatform
from bfbc2_masterserver.enumerators.theater.GameType import GameType
from bfbc2_masterserver.enumerators.theater.JoinMode import JoinMode

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.Persona import Persona
    from bfbc2_masterserver.models.theater.database.Lobby import Lobby


class Game(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    lobby: "Lobby" = Relationship(
        back_populates="games", sa_relationship_kwargs=dict(lazy="selectin")
    )
    lobbyId: int | None = Field(default=None, foreign_key="lobby.id")
    owner: "Persona" = Relationship(
        back_populates="games", sa_relationship_kwargs=dict(lazy="selectin")
    )
    ownerId: int | None = Field(default=None, foreign_key="persona.id")

    serverName: str

    addrIp: str
    addrPort: int

    joiningPlayers: int = 0
    queuedPlayers: int = 0
    activePlayers: int = 0
    maxPlayers: int = 0

    platform: ClientPlatform
    joinMode: JoinMode
    gameType: GameType

    serverSoftcore: bool = False
    serverHardcore: bool = False
    serverHasPassword: bool = False
    serverPunkbuster: bool = False
    serverEA: bool = False

    serverVersion: str
    clientVersion: str

    gameLevel: Optional[str] = None
    gameMod: Optional[str] = None
    gameMode: Optional[str] = None
    gameSGUID: Optional[int] = None
    gameTime: Optional[str] = None
    gameHash: Optional[str] = None
    gameRegion: Optional[str] = None
    gamePublic: bool = False
    gameElo: int = 0
    gameAutoBalance: bool = False
    gameBannerUrl: Optional[str] = None
    gameCrosshair: bool = False
    gameFriendlyFire: bool = False
    gameKillCam: bool = False
    gameMiniMap: bool = False
    gameMiniMapSpotting: bool = False
    gameThirdPersonVehicleCameras: bool = False
    gameThreeDSpotting: bool = False

    numObservers: int
    maxObservers: int

    providerId: Optional[str] = None
    queueLength: int
    punkbusterVersion: Optional[str] = None

    ugid: str
    ekey: str
    secret: str
