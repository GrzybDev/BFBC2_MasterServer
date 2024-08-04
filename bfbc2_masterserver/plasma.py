import asyncio
import logging
from base64 import b64encode

from fastapi import WebSocket

from bfbc2_masterserver.dataclasses.Handler import BaseHandler
from bfbc2_masterserver.dataclasses.Manager import BaseManager
from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLService import FESLService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.enumerators.fesl.MessageType import MessageType
from bfbc2_masterserver.error import TransactionError, TransactionSkip
from bfbc2_masterserver.message import HEADER_LENGTH, Message
from bfbc2_masterserver.messages.plasma.connect.Goodbye import GoodbyeRequest
from bfbc2_masterserver.messages.plasma.PlasmaError import PlasmaError
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.message.Chunk import Chunk
from bfbc2_masterserver.services.plasma.account import AccountService
from bfbc2_masterserver.services.plasma.association import AssociationService
from bfbc2_masterserver.services.plasma.connect import ConnectService
from bfbc2_masterserver.services.plasma.message import ExtensibleMessageService
from bfbc2_masterserver.services.plasma.playnow import PlayNowService
from bfbc2_masterserver.services.plasma.presence import PresenceService
from bfbc2_masterserver.services.plasma.ranking import RankingService
from bfbc2_masterserver.services.plasma.record import RecordService

logger = logging.getLogger(__name__)


class Plasma(BaseHandler):

    services: dict[FESLService, PlasmaService] = {}

    def __init__(self, manager: BaseManager, ws: WebSocket):
        """
        Initializes the Plasma object with a WebSocket.
        """
        self.manager: BaseManager = manager
        self.websocket: WebSocket = ws

        # Register services
        self.services[FESLService.ConnectService] = ConnectService(self)
        self.services[FESLService.AccountService] = AccountService(self)
        self.services[FESLService.AssociationService] = AssociationService(self)
        self.services[FESLService.MessageService] = ExtensibleMessageService(self)
        self.services[FESLService.PlayNowService] = PlayNowService(self)
        self.services[FESLService.PresenceService] = PresenceService(self)
        self.services[FESLService.RankingService] = RankingService(self)
        self.services[FESLService.RecordService] = RecordService(self)

    async def handle_transaction(
        self, message: Message, message_type: MessageType
    ) -> None:
        """
        Handles incoming transactions.

        Logs the incoming message, validates the service and transaction ID, and handles the request or response.

        Args:
            message (Message): The incoming message.
            message_type (MessageType): The type of the message (request or response).

        Raises:
            ValueError: If the service or transaction ID is invalid, or if the Plasma object is not initialized and the message type is not a request.
        """

        # Try to get the service from the message
        try:
            service = FESLService(message.service)
        except ValueError:
            # If the service is not valid, raise an error
            raise ValueError(f"Invalid service: {message.service}")

        # Get the transaction id from the message type
        tid: int = message.type & 0x00FFFFFF

        # If the Plasma object is not initialized and the service is ConnectService, set the transaction id
        if not hasattr(self, "connection") and service == FESLService.ConnectService:
            self.transactionID = tid

        # If the transaction id does not match the expected id
        if tid != self.transactionID:
            # If the message type is a response
            if message_type == MessageType.PlasmaResponse:
                # Simple transactions with a transaction id of 0 are unscheduled transactions (responses)
                # Check if this unscheduled transaction is allowed
                pass
            else:
                # If the transaction id is not valid, raise an error
                raise ValueError(
                    f"Invalid transaction id: {tid} (expected: {self.transactionID})"
                )

        response: TransactionError | TransactionSkip | Message

        # If the Plasma object is not initialized and the message type is not a request, set the response to an error
        if (
            not hasattr(self, "connection")
            and message_type != MessageType.PlasmaRequest
        ):
            response = self.finish_message(
                message, TransactionError(ErrorCode.NOT_INITIALIZED)
            )
        # If the message type is a request, handle the request
        elif message_type in [MessageType.PlasmaRequest, MessageType.PlasmaResponse]:
            response = self.services[service].handle(message)
        # If the message type is not valid, raise an error
        else:
            raise ValueError(f"Invalid message type: {message_type}")

        if isinstance(response, TransactionSkip):
            return
        elif isinstance(response, TransactionError):
            response = self.finish_message(message, response, noTransactionID=True)

        # Send the error message
        await self.__send(response)

        # Increment the transaction id for the next transaction
        self.transactionID += 1

    def finish_message(
        self, message: Message, response_data, noTransactionID=False
    ) -> Message:
        # Send the response
        if isinstance(response_data, TransactionError):
            # Prepare an error message
            response = Message()
            response.service = message.service
            response.type = MessageType.PlasmaResponse.value

            # If the Plasma object is not initialized, set the error message type to InitialError and add the transaction id
            if not hasattr(self, "connection"):
                response.type = MessageType.InitialError.value

            # Add the error details to the message
            response.data = PlasmaError(
                TXN=message.data.TXN,
                errorCode=ErrorCode(response_data.errorCode),
                localizedMessage=response_data.localizedMessage,
                errorContainer=response_data.errorContainer,
                TID=self.transactionID if not hasattr(self, "connection") else None,
            )
        else:
            # Prepare the response message
            response = Message()
            response.service = message.service
            response.type = MessageType.PlasmaResponse.value
            response.data = response_data
            response.data.TXN = message.data.TXN

        # If the message type is not an InitialError, add the transaction ID to the message type
        if response.type != MessageType.InitialError.value and not noTransactionID:
            response.type = response.type & 0xFF000000 | self.transactionID

        return response

    def start_transaction(
        self, service: FESLService, txn: FESLTransaction, data: PlasmaTransaction
    ) -> None:
        """
        Starts a transaction by getting the appropriate generator and calling it.

        Parameters:
            service (PlasmaService): The service associated with the transaction.
            txn (Transaction): The transaction to start.
            data (dict): The data for the transaction.
        """

        # Transactions started by the server are always "SimpleResponse" kind, and have no transaction ID

        # Prepare the message
        message = Message()
        message.service = service.value
        message.type = MessageType.PlasmaResponse.value
        message.data = PlasmaTransaction(TXN=txn)

        request = self.services[service].create_message(message, data)

        send_coroutine = self.__send(request)

        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        loop.create_task(send_coroutine)

    async def __send(self, message: Message) -> None:
        # Compile the response into bytes
        response_bytes = message.compile()

        # If the response is too big to send in one piece
        if len(response_bytes) > self.connection.fragmentSize:
            # Message is too big, we need to base64 encode it and split it into fragments
            message_bytes = response_bytes[HEADER_LENGTH:]  # Get rid of the header

            # Calculate the size of the message before and after encoding
            decoded_message_size: int = len(message_bytes)
            message_encoded: str = b64encode(message_bytes).decode()
            encoded_message_size: int = len(message_bytes)

            # Split the message into fragments of the maximum size
            fragments = [
                message_encoded[i : i + self.connection.fragmentSize]
                for i in range(0, len(message_encoded), self.connection.fragmentSize)
            ]

            # Send each fragment as a separate message
            for fragment in fragments:
                message_fragment = Message()
                message_fragment.service = message.service
                message_fragment.type = (
                    MessageType.PlasmaChunkedResponse.value & 0xFF000000
                    | self.transactionID
                )

                # Add the fragment and its size to the message
                message_fragment.data = Chunk(
                    data=fragment,
                    decodedSize=decoded_message_size,
                    size=encoded_message_size,
                )

                # Send the fragment
                await self.websocket.send_bytes(message_fragment.compile())
        else:
            # If the response fits into one message, send it
            await self.websocket.send_bytes(response_bytes)

    def disconnect(self, reason: int) -> None:
        self.start_transaction(
            FESLService.ConnectService,
            FESLTransaction.Goodbye,
            GoodbyeRequest(reason=reason),
        )

    def on_disconnect(self, reason: int | str, message: str | None) -> None:
        """
        Handles the client disconnecting.
        """

        if hasattr(self, "timerMemCheck"):
            self.timerMemCheck.cancel()

        if hasattr(self, "timerPing"):
            self.timerPing.cancel()

        if hasattr(self, "connection"):
            if hasattr(self.connection, "accountId"):
                self.manager.redis.delete(f"account:{self.connection.accountId}")

                if self.connection.type == ClientType.Client:
                    self.manager.CLIENTS.pop(self.connection.accountId, None)
                else:
                    if hasattr(self.connection, "gameId"):
                        self.manager.SERVERS.pop(self.connection.accountId, None)
                        self.manager.database.disable_game(self.connection.gameId)

                if self.connection.accountLoginKey:
                    self.manager.redis.delete(
                        f"session:{self.connection.accountLoginKey}"
                    )

                if self.connection.personaId:
                    self.manager.redis.delete(f"profile:{self.connection.personaId}")
                    self.manager.redis.delete(f"presence:{self.connection.personaId}")

                if self.connection.personaLoginKey:
                    self.manager.redis.delete(
                        f"persona:{self.connection.personaLoginKey}"
                    )

        if reason:
            logger.info(
                f"{self.get_client_address()}  -> Disconnected: {reason} ({message})"
            )
        else:
            logger.info(f"{self.get_client_address()}  -> Disconnected")
