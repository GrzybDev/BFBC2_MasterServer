from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GetStatsRequest(PlasmaTransaction):
    periodId: int
    periodPast: int
    keys: list[str]


class GetStatsResponse(PlasmaTransaction):
    pass
