from datetime import datetime

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Leaderboard import Leaderboard


class GetDateRangeRequest(PlasmaTransaction):
    key: str
    periodId: int


class GetDateRangeResponse(PlasmaTransaction):
    startDate: datetime
    endDate: datetime
