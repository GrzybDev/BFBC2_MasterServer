from pydantic import BaseModel


class Stat(BaseModel):
    key: str
    value: float


class RankedStat(BaseModel):
    key: str
    value: float
    rank: int


class RankedStatReturn(BaseModel):
    rankedStats: list[RankedStat]
    ownerId: int
    ownerType: int
