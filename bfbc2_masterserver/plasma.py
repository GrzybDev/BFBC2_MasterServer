import asyncio
import logging
from base64 import b64decode, b64encode
from pydoc import resolve

from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from pydantic import ValidationError

from bfbc2_masterserver.dataclasses.Client import Client
from bfbc2_masterserver.dataclasses.Connection import BaseConnection
from bfbc2_masterserver.dataclasses.Handler import BaseHandler, BasePlasmaHandler
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


class Plasma(BasePlasmaHandler):

    def __init__(self, manager: BaseManager, client: Client, ws: WebSocket):
        """
        Initializes the Plasma object with a WebSocket.
        """

        self.timerMemCheck = None
        self.timerPing = None

        self.manager: BaseManager = manager
        self.client: Client = client
        self.websocket: WebSocket = ws

        self.incoming_queue: list[Chunk] = []

        # Register services
        self.services: dict[FESLService, PlasmaService] = {}
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
        skipTIDCheck = False

        if not self.transactionID:
            if service == FESLService.ConnectService:
                skipTIDCheck = True

        # If the transaction id does not match the expected id
        if tid != self.transactionID and not skipTIDCheck:
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
        if not self.transactionID and service != FESLService.ConnectService:
            response = self.finish_message(
                message, TransactionError(ErrorCode.NOT_INITIALIZED)
            )
        # If the message type is a request, handle the request
        elif message_type in [MessageType.PlasmaRequest, MessageType.PlasmaResponse]:
            response = self.get_response(message)
        elif message_type in [
            MessageType.PlasmaChunkedRequest,
            MessageType.PlasmaChunkedResponse,
        ]:
            chunk = Chunk(**message.data)
            self.incoming_queue.append(chunk)

            received_length = sum([len(msg.data) for msg in self.incoming_queue])
            expected_length = chunk.size

            if received_length == expected_length:
                encoded_string = "".join([msg.data for msg in self.incoming_queue])
                decoded_string = b64decode(encoded_string).decode()
                self.incoming_queue.clear()

                message = Message(
                    service=service.value, type=message_type.value, data=decoded_string
                )

                response = self.get_response(message)
            else:
                return
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

    def get_response(
        self, message: Message
    ) -> TransactionError | TransactionSkip | Message:
        txn = message.data["TXN"]
        resolver, model = self.services[FESLService(message.service)]._get_resolver(txn)

        try:
            message.data = model.model_validate(message.data)

            # Log the incoming message
            logger.debug(f"{self.get_client_address()} -> {message}")
        except ValidationError as e:
            logger.exception(
                f"{self.get_client_address()} -> {e}",
                exc_info=True,
            )

            return TransactionError(ErrorCode.PARAMETERS_ERROR)

        response_data = resolver(message.data)

        if isinstance(response_data, TransactionSkip):
            return response_data
        elif isinstance(message.data, ValidationError):
            message.data = PlasmaTransaction(TXN=txn)

        response: Message = self.finish_message(message, response_data)

        # Log the outgoing message
        logger.debug(f"{self.get_client_address()} <- {response}")
        return response

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
            if self.transactionID is None:
                response.type = MessageType.InitialError.value

            # Add the error details to the message
            response.data = PlasmaError(
                TXN=(
                    message.data["TXN"]
                    if isinstance(message.data, dict)
                    else message.data.TXN
                ),
                errorCode=ErrorCode(response_data.errorCode),
                localizedMessage=response_data.localizedMessage,
                errorContainer=response_data.errorContainer,
                TID=self.transactionID if not self.transactionID else None,
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

        generator = self.services[service]._get_generator(txn.value)
        request = generator(data)

        finished_message: Message = self.finish_message(
            message, request, noTransactionID=True
        )

        # Log the outgoing message
        logger.debug(f"{self.get_client_address()} <- {finished_message}")

        send_coroutine = self.__send(finished_message)

        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        loop.create_task(send_coroutine)

    async def __send(self, message: Message) -> None:
        # Compile the response into bytes
        response_bytes = message.compile()

        if not self.client.connection.fragmentSize:
            raise RuntimeError("Fragment size is not set")

        # If the response is too big to send in one piece
        if len(response_bytes) > self.client.connection.fragmentSize:
            # Message is too big, we need to base64 encode it and split it into fragments
            message_bytes = response_bytes[HEADER_LENGTH:]  # Get rid of the header

            # Calculate the size of the message before and after encoding
            decoded_message_size: int = len(message_bytes)
            message_encoded: str = b64encode(message_bytes).decode()
            encoded_message_size: int = len(message_bytes)

            # Split the message into fragments of the maximum size
            fragments = [
                message_encoded[i : i + self.client.connection.fragmentSize]
                for i in range(
                    0, len(message_encoded), self.client.connection.fragmentSize
                )
            ]

            # Send each fragment as a separate message
            for fragment in fragments:
                message_fragment = Message()
                message_fragment.service = message.service

                if self.transactionID is None:
                    # We should never get here, as InitialError messages are not big enough to be fragmented
                    raise ValueError("Transaction ID is not set")

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
                try:
                    await self.websocket.send_bytes(message_fragment.compile())
                except RuntimeError as e:
                    self.on_disconnect(str(e), None)
        else:
            # If the response fits into one message, send it
            try:
                await self.websocket.send_bytes(response_bytes)
            except RuntimeError as e:
                self.on_disconnect(str(e), None)

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

        if self.timerMemCheck:
            self.timerMemCheck.cancel()

        if self.timerPing:
            self.timerPing.cancel()

        if (
            self.client.connection.account
            and self.client.connection.type == ClientType.Client
        ):
            self.manager.CLIENTS.pop(self.client.connection.account.id, None)

        if self.client.connection.persona and self.client.connection.personaSession:
            self.manager.redis.delete(f"client:{self.client.connection.personaSession}")
            self.manager.redis.delete(f"presence:{self.client.connection.persona.id}")

        if self.client.connection.game:
            self.manager.database.game_disable(self.client.connection.game.id)

        if reason:
            logger.info(
                f"{self.get_client_address()}  -> Disconnected: {reason} ({message})"
            )
        else:
            logger.info(f"{self.get_client_address()}  -> Disconnected")
