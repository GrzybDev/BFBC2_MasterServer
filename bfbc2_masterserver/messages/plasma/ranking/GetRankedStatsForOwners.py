from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Owner import RankedOwner
from bfbc2_masterserver.models.plasma.Stats import RankedOwnerStat


class GetRankedStatsForOwnersRequest(PlasmaTransaction):
    owners: list[RankedOwner]
    keys: list[str]
    periodId: int


class GetRankedStatsForOwnersResponse(PlasmaTransaction):
    rankedStats: list[RankedOwnerStat]
