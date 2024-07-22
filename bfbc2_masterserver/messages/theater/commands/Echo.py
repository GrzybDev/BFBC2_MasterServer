from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class EchoRequest(TheaterTransaction):
    TYPE: int
    UID: int


class EchoResponse(TheaterTransaction):
    TXN: str
    IP: str
    PORT: int
    ERR: int
    TYPE: int
