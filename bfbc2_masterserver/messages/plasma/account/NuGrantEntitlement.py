from datetime import datetime
from typing import Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuGrantEntitlementRequest(PlasmaTransaction):
    entitlementTag: Optional[str] = None
    groupName: Optional[str] = None
    productCatalog: Optional[str] = None
    productId: Optional[str] = None
    grantStartDate: Optional[datetime] = None
    grantEndDate: Optional[datetime] = None
    entitlementType: Optional[str] = None
    devicePhysicalId: Optional[str] = None
    deviceType: Optional[str] = None
    gamerTag: Optional[str] = None
    masterId: int
    personaId: Optional[int] = None


class NuGrantEntitlementResponse(PlasmaTransaction):
    pass
