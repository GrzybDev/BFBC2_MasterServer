from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.messages.Stats import RankedStat


class GetRankedStatsRequest(PlasmaTransaction):
    owner: int
    ownerType: int
    periodId: int
    periodPast: int
    keys: list[str]
    rankOrders: list[int]


class GetRankedStatsResponse(PlasmaTransaction):
    stats: list[RankedStat]
