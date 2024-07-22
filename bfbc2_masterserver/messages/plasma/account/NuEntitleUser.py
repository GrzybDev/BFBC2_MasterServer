from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.database.Entitlement import Entitlement


class NuEntitleUserRequest(PlasmaTransaction):
    key: str


class NuEntitleUserResponse(PlasmaTransaction):
    productList: list[Entitlement]
