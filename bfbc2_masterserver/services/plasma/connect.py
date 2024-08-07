import asyncio
import random
import string
from datetime import datetime

from bfbc2_masterserver.dataclasses.Connection import BaseConnection
from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLService import FESLService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError, TransactionSkip
from bfbc2_masterserver.messages.plasma.connect.GetPingSites import (
    GetPingSitesRequest,
    GetPingSitesResponse,
)
from bfbc2_masterserver.messages.plasma.connect.Goodbye import GoodbyeRequest
from bfbc2_masterserver.messages.plasma.connect.Hello import HelloRequest, HelloResponse
from bfbc2_masterserver.messages.plasma.connect.MemCheck import (
    MemCheckRequest,
    MemCheckResult,
)
from bfbc2_masterserver.messages.plasma.connect.Ping import PingRequest, PingResponse
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.DomainPartition import DomainPartition
from bfbc2_masterserver.models.plasma.MemCheck import MemCheck
from bfbc2_masterserver.settings import (
    CLIENT_INITIAL_MEMCHECK_INTERVAL,
    CLIENT_MEMCHECK_INTERVAL,
    CLIENT_PING_INTERVAL,
    MESSENGER_HOST,
    MESSENGER_PORT,
    SERVER_INITIAL_MEMCHECK_INTERVAL,
    SERVER_MEMCHECK_INTERVAL,
    SERVER_PING_INTERVAL,
    THEATER_CLIENT_PORT,
    THEATER_HOST,
    THEATER_SERVER_PORT,
)


class ConnectService(PlasmaService):
    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[FESLTransaction.Hello] = self.__handle_hello, HelloRequest
        self.resolvers[FESLTransaction.MemCheck] = (
            self.__handle_memcheck,
            MemCheckResult,
        )
        self.resolvers[FESLTransaction.GetPingSites] = (
            self.__handle_get_ping_sites,
            GetPingSitesRequest,
        )
        self.resolvers[FESLTransaction.Ping] = self.__handle_ping, PingResponse
        self.resolvers[FESLTransaction.Goodbye] = (
            self.__handle_goodbye,
            GoodbyeRequest,
        )
        self.resolvers[FESLTransaction.Suicide] = (
            self.__handle_suicide,
            PlasmaTransaction,
        )

        self.generators[FESLTransaction.MemCheck] = self.__create_memcheck
        self.generators[FESLTransaction.Ping] = self.__create_ping
        self.generators[FESLTransaction.Goodbye] = self.__create_goodbye

    def _get_resolver(self, txn):
        """
        Gets the resolver for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The resolver function for the transaction.
        """
        return self.resolvers[FESLTransaction(txn)]

    def _get_generator(self, txn):
        """
        Gets the generator for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The generator function for the transaction.
        """
        return self.generators[FESLTransaction(txn)]

    def __handle_hello(self, data: HelloRequest) -> HelloResponse | TransactionError:
        """
        Handles the initial packet sent by client, used to determine client type, and other connection details

        This method is used to determine the client type and other connection details. If the Plasma object is already initialized, a system error is returned. Otherwise, the data is validated and the Plasma object is initialized.

        Parameters:
            data (dict): The incoming data.

        Returns:
            A TransactionError if the Plasma object is already initialized or if the data is invalid.
            A HelloResponse if the data is valid.
        """

        if self.connection.fragmentSize:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        self.connection.clientName = data.clientString
        self.connection.clientVersion = data.clientVersion
        self.connection.locale = data.locale
        self.connection.platform = data.clientPlatform
        self.connection.type = data.clientType
        self.connection.fragmentSize = data.fragmentSize
        self.plasma.transactionID = 1

        theater_ip = THEATER_HOST.format(clientString=data.clientString)
        theater_port = (
            THEATER_CLIENT_PORT
            if data.clientType == ClientType.Client
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
            messengerIp=MESSENGER_HOST,
            messengerPort=MESSENGER_PORT,
            theaterIp=theater_ip,
            theaterPort=theater_port,
        )

        # Client also supports "addressRemapping" value here, but it's never sent by the original server
        # response.addressRemapping = "\0"
        # If not set, client will set this value to NULL internally (just like above)
        # No clue what this value is used for

        # Activate both ping and memcheck timers
        loop = asyncio.get_event_loop()

        self.plasma.timerPing = loop.call_later(
            (
                CLIENT_PING_INTERVAL
                if data.clientType == ClientType.Client
                else SERVER_PING_INTERVAL
            ),
            self.__make_ping,
        )

        self.plasma.timerMemCheck = loop.call_later(
            (
                CLIENT_INITIAL_MEMCHECK_INTERVAL
                if data.clientType == ClientType.Client
                else SERVER_INITIAL_MEMCHECK_INTERVAL
            ),
            self.__make_memcheck,
        )

        # Start the MemCheck
        self.__make_memcheck()
        return response

    def __create_memcheck(self, data: dict) -> MemCheckRequest:
        """
        Creates a memcheck request
        """
        request = MemCheckRequest(
            memcheck=MemCheck(),
            type=0,
            salt="".join(random.choice(string.digits) for _ in range(10)),
        )

        return request

    def __handle_memcheck(self, data: MemCheckResult) -> TransactionSkip:
        """
        Handles the memcheck request
        """

        return TransactionSkip()

    def __make_ping(self) -> None:
        self.plasma.start_transaction(
            FESLService.ConnectService, FESLTransaction.Ping, PlasmaTransaction()
        )

        loop = asyncio.get_event_loop()
        self.plasma.timerPing = loop.call_later(
            (
                CLIENT_PING_INTERVAL
                if self.plasma.client.connection.type == ClientType.Client
                else SERVER_PING_INTERVAL
            ),
            self.__make_ping,
        )

    def __make_memcheck(self) -> None:
        self.plasma.start_transaction(
            FESLService.ConnectService, FESLTransaction.MemCheck, PlasmaTransaction()
        )

        loop = asyncio.get_event_loop()
        self.plasma.timerMemCheck = loop.call_later(
            (
                CLIENT_MEMCHECK_INTERVAL
                if self.plasma.client.connection.type == ClientType.Client
                else SERVER_MEMCHECK_INTERVAL
            ),
            self.__make_memcheck,
        )

    def __handle_get_ping_sites(
        self, data: GetPingSitesRequest
    ) -> GetPingSitesResponse:
        """
        Handles the request for ping sites

        This method is used to determine the ping sites to send to the client. The original server always sends 4 ping sites, but we don't have any ping sites to send, so we just return an empty list.

        Parameters:
            data (dict): The incoming data.

        Returns:
            A GetPingSitesResponse with an empty list of ping sites.
        """

        # Original server always sends 4 ping sites
        # {
        #    "name": "nrt",
        #    "type": 0,
        #    "addr": "109.200.220.1"
        # }
        # {
        #    "name": "gva",
        #    "type": 0,
        #    "addr": "159.153.72.181"
        # }
        # {
        #    "name": "sjc",
        #    "type": 0,
        #    "addr": "159.153.70.181"
        # }
        # {
        #    "name": "iad",
        #    "type": 0,
        #    "addr": "159.153.93.213"
        # }

        # Not sure what ping sites are nor how do they affect the client
        # But original server always sends the above 4 ping sites
        # We don't have any ping sites to send so we just return an empty list

        ping_sites = []
        return GetPingSitesResponse(pingSite=ping_sites, minPingSitesToPing=0)

    def __create_ping(self, data: PingRequest) -> PingResponse:
        """
        Creates a ping request
        """

        return PingResponse()

    def __handle_ping(self, data: PingRequest) -> TransactionSkip:
        """
        Handles the ping request
        """

        return TransactionSkip()

    def __handle_goodbye(self, data: GoodbyeRequest) -> TransactionSkip:
        """
        Handles the goodbye request
        """

        self.plasma.on_disconnect(reason=data.reason, message=data.message)

        return TransactionSkip()

    def __handle_suicide(self, data: dict):
        """
        Client support this message, but I'm not sure what this Transaction is supposed to do,
        we ignore it - never captured this packet from original master server so I suppose it's another leftover.
        """

        raise NotImplementedError()

    def __create_goodbye(self, data: GoodbyeRequest):
        return data
