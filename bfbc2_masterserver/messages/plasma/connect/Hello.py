import datetime
from typing import Optional

from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale
from bfbc2_masterserver.enumerators.client.ClientPlatform import ClientPlatform
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.messages.plasma.DomainPartition import DomainPartition
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class HelloRequest(PlasmaTransaction):
    clientString: str
    sku: str
    locale: ClientLocale
    clientPlatform: ClientPlatform
    clientVersion: str
    SDKVersion: str
    protocolVersion: str
    fragmentSize: int
    clientType: ClientType


class HelloResponse(PlasmaTransaction):
    activityTimeoutSecs: int
    curTime: datetime.datetime
    domainPartition: DomainPartition
    messengerIp: str
    messengerPort: int
    theaterIp: str
    theaterPort: int
    addressRemapping: Optional[str] = None
