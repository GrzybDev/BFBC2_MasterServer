from pydantic import BaseModel, Field


class GameServer(BaseModel):
    LID: int
    GID: int
    MAX_PLAYERS: int = Field(alias="MAX-PLAYERS")
    EKEY: str
    UGID: str
    JOIN: str
    SECRET: str
    J: str
