from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Owner import RankedOwner
from bfbc2_masterserver.models.plasma.Stats import Stat


class GetStatsForOwnersRequest(PlasmaTransaction):
    owners: list[RankedOwner]
    keys: list[str]


class GetStatsForOwnersResponse(PlasmaTransaction):
    stats: list[Stat]
