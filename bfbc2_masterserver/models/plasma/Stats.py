from decimal import Decimal

from pydantic import BaseModel


class Stat(BaseModel):
    key: str
    value: Decimal


class RankedStat(Stat):
    rank: int


class RankedOwnerStat(BaseModel):
    rankedStats: list[RankedStat]
    ownerId: int
    ownerType: int
