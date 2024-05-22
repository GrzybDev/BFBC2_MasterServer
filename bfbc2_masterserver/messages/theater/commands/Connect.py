from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale
from bfbc2_masterserver.enumerators.client.ClientPlatform import ClientPlatform
from bfbc2_masterserver.messages.theater.TheaterMessage import TheaterMessage


class ConnectRequest(TheaterMessage):
    PROT: int
    PROD: str
    VERS: str
    PLAT: ClientPlatform
    LOCALE: ClientLocale
    SDKVERSION: str


class ConnectResponse(TheaterMessage):
    TIME: int
    activityTimeoutSecs: int
    PROT: int
