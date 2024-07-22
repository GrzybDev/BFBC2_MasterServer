from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class UpdateBracketRequest(TheaterTransaction):
    START: bool


class UpdateBracketResponse(TheaterTransaction):
    pass
