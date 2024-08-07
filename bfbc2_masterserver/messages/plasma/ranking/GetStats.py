from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Stats import Stat


class GetStatsRequest(PlasmaTransaction):
    periodId: int
    periodPast: int
    keys: list[str]


class GetStatsResponse(PlasmaTransaction):
    stats: list[Stat]
