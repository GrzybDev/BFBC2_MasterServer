from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Leaderboard import Leaderboard


class GetTopNRequest(PlasmaTransaction):
    key: str
    minRank: int
    maxRank: int


class GetTopNResponse(PlasmaTransaction):
    stats: list[Leaderboard]
