from bfbc2_masterserver.messages.theater.TheaterMessage import TheaterMessage


class EchoRequest(TheaterMessage):
    TYPE: int
    UID: int


class EchoResponse(TheaterMessage):
    TXN: str
    IP: str
    PORT: int
    ERR: int
    TYPE: int
