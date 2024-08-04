from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale
from bfbc2_masterserver.enumerators.client.ClientPlatform import ClientPlatform
from bfbc2_masterserver.enumerators.client.ClientType import ClientType


class BaseConnection:
    clientName: str
    locale: ClientLocale
    platform: ClientPlatform
    type: ClientType
    fragmentSize: int

    accountId: int
    accountLoginKey: str
    personaName: str
    personaId: int
    personaLoginKey: str
    gameId: int

    internalIp: str
    internalPort: int
