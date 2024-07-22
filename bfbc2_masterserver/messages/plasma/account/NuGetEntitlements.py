from typing import Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.database.Entitlement import Entitlement


class NuGetEntitlementsRequest(PlasmaTransaction):
    status: str
    groupName: str
    entitlementTag: Optional[str] = None
    masterUserId: Optional[int] = None


class NuGetEntitlementsResponse(PlasmaTransaction):
    entitlements: list[Entitlement]
