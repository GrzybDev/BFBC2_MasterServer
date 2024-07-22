import datetime
from typing import Optional

from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale
from bfbc2_masterserver.enumerators.client.ClientPlatform import ClientPlatform
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.DomainPartition import DomainPartition


class HelloRequest(PlasmaTransaction):
    """
    The HelloRequest class is a subclass of the PlasmaTransaction class.

    This class represents a Hello request in the Plasma system. It includes various attributes related to the client and the request.

    Attributes:
        clientString (str): The client string.
        sku (str): The SKU of the client.
        locale (ClientLocale): The locale of the client.
        clientPlatform (ClientPlatform): The platform of the client.
        clientVersion (str): The version of the client.
        SDKVersion (str): The version of the SDK used by the client.
        protocolVersion (str): The version of the protocol used by the client.
        fragmentSize (int): The size of the fragment.
        clientType (ClientType): The type of the client.
    """

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
    """
    The HelloResponse class is a subclass of the PlasmaTransaction class.

    This class represents a Hello response in the Plasma system. It includes various attributes related to the response.

    Attributes:
        activityTimeoutSecs (int): The activity timeout in seconds.
        curTime (datetime.datetime): The current time.
        domainPartition (DomainPartition): The domain partition.
        messengerIp (str): The IP address of the messenger.
        messengerPort (int): The port of the messenger.
        theaterIp (str): The IP address of the theater.
        theaterPort (int): The port of the theater.
        addressRemapping (Optional[str]): The address remapping. This attribute is optional and defaults to None.
    """

    activityTimeoutSecs: int
    curTime: datetime.datetime
    domainPartition: DomainPartition
    messengerIp: str
    messengerPort: int
    theaterIp: str
    theaterPort: int
    addressRemapping: Optional[str] = None
