from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.messages.Stats import Stat


class GetStatsRequest(PlasmaTransaction):
    periodId: int
    periodPast: int
    keys: list[str]


class GetStatsResponse(PlasmaTransaction):
    stats: list[Stat]
