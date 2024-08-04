from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class EnterGameHostResponse(TheaterTransaction):
    LID: int
    GID: int
    PID: int

    ALLOWED: bool
