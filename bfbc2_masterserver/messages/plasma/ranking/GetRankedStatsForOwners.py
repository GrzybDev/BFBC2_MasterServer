from bfbc2_masterserver.messages.plasma.Owner import RankedOwner
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.messages.Stats import RankedStat, RankedStatReturn, Stat


class GetRankedStatsForOwnersRequest(PlasmaTransaction):
    owners: list[RankedOwner]
    keys: list[str]
    periodId: int


class GetRankedStatsForOwnersResponse(PlasmaTransaction):
    rankedStats: list[RankedStatReturn]
