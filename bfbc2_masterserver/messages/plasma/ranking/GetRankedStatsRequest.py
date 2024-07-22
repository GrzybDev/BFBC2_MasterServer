from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.database.Stats import RankedStat


class GetRankedStatsRequest(PlasmaTransaction):
    owner: int
    ownerType: int
    periodId: int
    periodPast: int
    keys: list[str]
    rankOrders: list[int]


class GetRankedStatsResponse(PlasmaTransaction):
    stats: list[RankedStat]
