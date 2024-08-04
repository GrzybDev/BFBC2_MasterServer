from typing import Optional

from pydantic import BaseModel, Field, IPvAnyAddress


class GameServer(BaseModel):
    LID: int
    GID: int

    serverName: str

    addrIp: IPvAnyAddress
    addrPort: int

    joiningPlayers: int
    queuedPlayers: int
    activePlayers: int
    maxPlayers: int

    platform: str
    joinMode: str
    gameType: str

    serverSoftcore: bool
    serverHardcore: bool
    serverHasPassword: bool
    serverPunkbuster: bool
    serverEA: bool

    serverVersion: str
    clientVersion: str

    gameLevel: Optional[str]
    gameMod: Optional[str]
    gameMode: Optional[str]
    gameSGUID: Optional[int]
    gameTime: Optional[str]
    gameHash: Optional[str]
    gameRegion: Optional[str]
    gamePublic: bool
    gameElo: int
    gameAutoBalance: bool
    gameBannerUrl: Optional[str]
    gameCrosshair: bool
    gameFriendlyFire: bool
    gameKillCam: bool
    gameMiniMap: bool
    gameMiniMapSpotting: bool
    gameThirdPersonVehicleCameras: bool
    gameThreeDSpotting: bool

    numObservers: int
    maxObservers: int

    providerId: Optional[str]
    queueLength: int
    punkbusterVersion: Optional[str]

    ugid: str
    ekey: str
    secret: str

    playerData: list[str]
    serverDescriptions: list[str]
