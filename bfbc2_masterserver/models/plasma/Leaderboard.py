from pydantic import BaseModel

from bfbc2_masterserver.models.plasma.database.Stats import Stat


class Leaderboard(BaseModel):
    addStats: list[Stat]
