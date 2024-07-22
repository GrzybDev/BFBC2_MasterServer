from pydantic import BaseModel


class Stat(BaseModel):
    key: str
    value: float


class RankedStat(Stat):
    rank: int


class RankedOwnerStat(BaseModel):
    rankedStats: list[RankedStat]
    ownerId: int
    ownerType: int
