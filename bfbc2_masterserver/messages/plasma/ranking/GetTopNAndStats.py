from pydantic import BaseModel

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.messages.Stats import Stat


class Leaderboard(BaseModel):
    addStats: list[Stat]


class GetTopNAndStatsRequest(PlasmaTransaction):
    key: str
    ownerType: int
    minRank: int
    maxRank: int
    periodId: int
    periodPast: int
    rankOrder: int
    keys: list[str]


class GetTopNAndStatsResponse(PlasmaTransaction):
    stats: list[Leaderboard]
