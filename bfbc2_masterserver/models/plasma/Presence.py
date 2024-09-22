from pydantic import BaseModel

from bfbc2_masterserver.models.plasma.Owner import Owner


class PresenceRequest(BaseModel):
    userId: int


class PresenceResponse(BaseModel):
    owner: Owner
    outcome: int
