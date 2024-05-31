from datetime import datetime

from pydantic import BaseModel


class Entitlement(BaseModel):
    grantDate: datetime
    groupName: str
    userId: int
    entitlementTag: str
    version: int
    terminationDate: datetime
    productId: str
    entitlementId: str
    status: str
