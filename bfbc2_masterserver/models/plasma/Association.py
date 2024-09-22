from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from bfbc2_masterserver.models.plasma.Owner import Owner


class AssociationRequest(BaseModel):
    owner: Owner
    member: Owner
    mutual: bool


class AssociationReturn(BaseModel):
    id: int
    name: str
    type: int
    created: Optional[datetime]
    modified: Optional[datetime]


class AssociationResult(BaseModel):
    member: AssociationReturn
    owner: Owner
    mutual: bool
    outcome: int
    listSize: int
