from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Stats import RankedOwnerStat, UserUpdateRequest


class UpdateStatsRequest(PlasmaTransaction):
    u: list[UserUpdateRequest]


class UpdateStatsResponse(PlasmaTransaction):
    pass
