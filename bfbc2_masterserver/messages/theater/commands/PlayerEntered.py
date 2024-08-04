from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class PlayerEnteredRequest(TheaterTransaction):
    LID: int
    GID: int
    PID: int


class PlayerEnteredResponse(TheaterTransaction):
    PID: int
