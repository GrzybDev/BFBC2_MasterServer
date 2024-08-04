from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class PlayerExitedRequest(TheaterTransaction):
    LID: int
    GID: int
    PID: int


class PlayerExitedResponse(TheaterTransaction):
    pass
