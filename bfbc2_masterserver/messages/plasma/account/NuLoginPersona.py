from pydantic import BaseModel


class NuLoginPersonaRequest(BaseModel):
    name: str


class NuLoginPersonaResponse(BaseModel):
    lkey: str
    profileId: str
    userId: str
