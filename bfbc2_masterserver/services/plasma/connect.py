from datetime import datetime
from enum import Enum

from pydantic import ValidationError

from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.messages.plasma.connect.Hello import HelloRequest, HelloResponse
from bfbc2_masterserver.messages.plasma.DomainPartition import DomainPartition
from bfbc2_masterserver.services.service import Service
from bfbc2_masterserver.settings import (
    MESSENGER_IP,
    MESSENGER_PORT,
    THEATER_CLIENT_PORT,
    THEATER_HOST,
    THEATER_SERVER_PORT,
)


class TXN(Enum):
    Hello = "Hello"
    Ping = "Ping"
    Goodbye = "Goodbye"
    Suicide = "Suicide"
    MemCheck = "MemCheck"
    GetPingSites = "GetPingSites"


class ConnectService(Service):
    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[TXN.Hello] = self.__handle_hello

    def _get_resolver(self, txn):
        return self.resolvers[TXN(txn)]

    def _get_generator(self, txn):
        return self.generators[TXN(txn)]

    def __handle_hello(self, data):
        """Initial packet sent by client, used to determine client type, and other connection details"""

        if self.plasma.initialized:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        try:
            data = HelloRequest.model_validate(data)
        except ValidationError:
            return TransactionError(ErrorCode.PARAMETERS_ERROR)

        self.plasma.initialized = True
        self.plasma.fragmentSize = data.fragmentSize

        theater_ip = THEATER_HOST.format(clientString=data.clientString)
        theater_port = (
            THEATER_CLIENT_PORT
            if data.clientType == ClientType.CLIENT
            else THEATER_SERVER_PORT
        )

        domainPartition = DomainPartition(
            domain="eagames",
            subDomain="BFBC2",
        )

        response = HelloResponse(
            activityTimeoutSecs=0,  # Client sets this to 200 (3.33 minutes) if set to 0
            curTime=datetime.now(),
            domainPartition=domainPartition,  # Game doesn't seem to care about this, but it's sent by the original server
            messengerIp=MESSENGER_IP,
            messengerPort=MESSENGER_PORT,
            theaterIp=theater_ip,
            theaterPort=theater_port,
        )

        # Client also supports "addressRemapping" value here, but it's never sent by the original server
        # response.addressRemapping = "\0"
        # If not set, client will set this value to NULL internally (just like above)
        # No clue what this value is used for

        message = Message(data=response.model_dump(exclude_none=True))
        return message
