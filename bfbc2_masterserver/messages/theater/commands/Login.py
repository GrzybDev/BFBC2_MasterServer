from bfbc2_masterserver.messages.theater.TheaterMessage import TheaterMessage


class LoginRequest(TheaterMessage):
    CID: str
    MAC: str
    SKU: str
    LKEY: str
    NAME: str


class LoginResponse(TheaterMessage):
    NAME: str
