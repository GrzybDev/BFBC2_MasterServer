from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class LoginRequest(TheaterTransaction):
    CID: str
    MAC: str
    SKU: str
    LKEY: str
    NAME: str


class LoginResponse(TheaterTransaction):
    NAME: str
