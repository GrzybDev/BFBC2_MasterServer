from decimal import Decimal

from pydantic import BaseModel

from bfbc2_masterserver.enumerators.plasma.StatUpdateType import StatUpdateType


class Stat(BaseModel):
    key: str
    value: Decimal


class RankedStat(Stat):
    rank: int


class RankedOwnerStat(BaseModel):
    rankedStats: list[RankedStat]
    ownerId: int
    ownerType: int


class StatUpdate(BaseModel):
    ut: StatUpdateType
    k: str
    v: Decimal


class UserUpdateRequest(BaseModel):
    o: int
    s: list[StatUpdate]
