from bfbc2_masterserver.messages.theater.TheaterMessage import TheaterMessage


class UpdateBracketRequest(TheaterMessage):
    START: bool


class UpdateBracketResponse(TheaterMessage):
    pass
