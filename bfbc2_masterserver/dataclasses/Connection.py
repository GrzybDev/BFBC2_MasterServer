from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale
from bfbc2_masterserver.enumerators.client.ClientType import ClientType


class BaseConnection:
    clientName: str
    locale: ClientLocale
    type: ClientType
    fragmentSize: int

    accountId: int
    accountLoginKey: str
    personaId: int
    personaLoginKey: str
