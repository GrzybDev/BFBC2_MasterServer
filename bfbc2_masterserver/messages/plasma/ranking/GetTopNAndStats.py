from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Leaderboard import Leaderboard


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
