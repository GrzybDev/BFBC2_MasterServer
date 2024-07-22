from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale
from bfbc2_masterserver.enumerators.client.ClientPlatform import ClientPlatform
from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class ConnectRequest(TheaterTransaction):
    PROT: int
    PROD: str
    VERS: str
    PLAT: ClientPlatform
    LOCALE: ClientLocale
    SDKVERSION: str


class ConnectResponse(TheaterTransaction):
    TIME: int
    activityTimeoutSecs: int
    PROT: int
