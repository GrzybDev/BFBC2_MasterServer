from bfbc2_masterserver.messages.plasma.Entitlement import Entitlement
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuEntitleUserRequest(PlasmaTransaction):
    key: str


class NuEntitleUserResponse(PlasmaTransaction):
    productList: list[Entitlement]
