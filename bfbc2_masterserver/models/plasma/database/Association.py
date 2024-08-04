from datetime import datetime

from pydantic import BaseModel

from bfbc2_masterserver.models.plasma.Owner import Owner


class Association(BaseModel):
    id: int
    name: str
    type: int
    created: datetime
    modified: datetime


class AssocationRequest(BaseModel):
    owner: Owner
    member: Owner
    mutual: bool
