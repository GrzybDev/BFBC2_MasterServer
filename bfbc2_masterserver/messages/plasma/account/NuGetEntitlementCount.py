from typing import Optional

from pydantic import Field

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuGetEntitlementCountRequest(PlasmaTransaction):
    entitlementId: Optional[str]
    entitlementTag: Optional[str]
    masterUserId: Optional[int]
    userId: Optional[int]
    global_: Optional[str] = Field(alias="global")
    status: Optional[str]
    groupName: Optional[str]
    productCatalog: Optional[str]
    productId: Optional[str]
    grantStartDate: Optional[str]
    grantEndDate: Optional[str]
    projectId: Optional[str]
    entitlementType: Optional[str]
    devicePhysicalId: Optional[str]


class NuGetEntitlementCountResponse(PlasmaTransaction):
    entitlementCount: int
