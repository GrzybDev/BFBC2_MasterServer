from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Entitlement(BaseModel):
    userId: int
    groupName: str | None
    entitlementId: int | None
    entitlementTag: str | None
    productId: str | None
    version: int
    grantDate: datetime | None
    terminationDate: Optional[datetime] = None
    statusReasonCode: Optional[str] = None
    status: str
