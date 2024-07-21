from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Entitlement(BaseModel):
    grantDate: datetime
    groupName: str
    userId: int
    entitlementTag: str
    version: int
    terminationDate: Optional[datetime]
    productId: Optional[str] = None
    entitlementId: str
    status: str
