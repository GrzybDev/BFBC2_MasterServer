from typing import Optional

from bfbc2_masterserver.messages.plasma.Entitlement import Entitlement
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuGetEntitlementsRequest(PlasmaTransaction):
    status: str
    groupName: str
    entitlementTag: Optional[str] = None
    masterUserId: Optional[int] = None


class NuGetEntitlementsResponse(PlasmaTransaction):
    entitlements: list[Entitlement]
