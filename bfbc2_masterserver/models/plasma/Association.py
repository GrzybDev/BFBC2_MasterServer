from datetime import datetime

from pydantic import BaseModel

from bfbc2_masterserver.models.plasma.Owner import Owner


class AssociationReturn(BaseModel):
    id: int
    name: str
    type: int
    created: datetime
    modified: datetime


class AssociationRequest(BaseModel):
    owner: Owner
    member: Owner
    mutual: bool
