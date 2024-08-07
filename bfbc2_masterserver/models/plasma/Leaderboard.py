from pydantic import BaseModel

from bfbc2_masterserver.models.plasma.Stats import Stat


class Leaderboard(BaseModel):
    addStats: list[Stat]
    owner: int
    name: str
    rank: int
