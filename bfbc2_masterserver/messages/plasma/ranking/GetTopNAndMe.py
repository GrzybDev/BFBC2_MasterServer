from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Leaderboard import Leaderboard


class GetTopNAndMeRequest(PlasmaTransaction):
    key: str
    minRank: int
    maxRank: int


class GetTopNAndMeResponse(PlasmaTransaction):
    stats: list[Leaderboard]
