from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class LeaveGameRequest(TheaterTransaction):
    LID: int
    GID: int


class LeaveGameResponse(TheaterTransaction):
    LID: int
    GID: int
