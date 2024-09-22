from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Owner import Owner


class NuSearchOwnersRequest(PlasmaTransaction):
    screenName: str


class NuSearchOwnersResponse(PlasmaTransaction):
    users: list[Owner]
    nameSpaceId: str  # "battlefield"
