import asyncio
import logging
from base64 import b64encode

from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.message.MessageType import MessageType
from bfbc2_masterserver.enumerators.plasma.PlasmaService import PlasmaService
from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.error import TransactionError, TransactionSkip
from bfbc2_masterserver.message import HEADER_LENGTH, Message
from bfbc2_masterserver.messages.plasma.PlasmaChunk import PlasmaChunk
from bfbc2_masterserver.messages.plasma.PlasmaError import PlasmaError
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.services.plasma.account import AccountService
from bfbc2_masterserver.services.plasma.connect import ConnectService

logger = logging.getLogger(__name__)


class Plasma:
    """
    A class to manage Plasma transactions.

    Attributes:
        services (dict): A dictionary to store services.
        initialized (bool): A flag to check if the Plasma object is initialized.
        fragmentSize (int): Size of the fragment.
        transactionID (int): ID of the transaction.
        ws (WebSocket): The WebSocket object used for communication.

    Methods:
        __init__(self, ws): Initializes the Plasma object with a WebSocket.
        handle_transaction(self, message: Message, message_type: MessageType): Handles incoming transactions.
    """

    services = {}

    initialized = False

    disconnectReason = None
    disconnectMessage = None

    clientString: str
    clientLocale: ClientLocale
    clientType: ClientType
    fragmentSize: int

    accountID: int | None = None
    profileID: int | None = None
    loginKey: str | None = None
    profileLoginKey: str | None = None

    transactionID: int

    timerPing: asyncio.TimerHandle
    timerMemCheck: asyncio.TimerHandle

    def __init__(self, manager, ws):
        """
        Initializes the Plasma object with a WebSocket.
        """
        self.manager = manager
        self.ws = ws

        # Register services
        self.services[PlasmaService.ConnectService] = ConnectService(self)
        self.services[PlasmaService.AccountService] = AccountService(self)

    async def handle_transaction(self, message: Message, message_type: MessageType):
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
            service = PlasmaService(message.service)
        except ValueError:
            # If the service is not valid, raise an error
            raise ValueError(f"Invalid service: {message.service}")

        # Get the transaction id from the message type
        tid = message.type & 0x00FFFFFF

        # If the Plasma object is not initialized and the service is ConnectService, set the transaction id
        if not self.initialized and service == PlasmaService.ConnectService:
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

        # If the Plasma object is not initialized and the message type is not a request, set the response to an error
        if not self.initialized and message_type != MessageType.PlasmaRequest:
            response = self.finish_message(
                message, TransactionError(ErrorCode.NOT_INITIALIZED)
            )
        # If the message type is a request, handle the request
        elif message_type in [MessageType.PlasmaRequest, MessageType.PlasmaResponse]:
            response = self.services[service].handle(message)
        # If the message type is not valid, raise an error
        else:
            raise ValueError(f"Invalid message type: {message_type}")

        # If the response is None, raise an error
        if response is None:
            raise ValueError("Response is None")
        # If the response is a TransactionSkip, return without doing anything
        elif isinstance(response, TransactionSkip):
            return

        # Send the error message
        await self.__send(response)

        # Increment the transaction id for the next transaction
        self.transactionID += 1

    def finish_message(self, message: Message, response_data, noTransactionID=False):
        # Send the response
        if isinstance(response_data, TransactionError):
            # Prepare an error message
            response = Message()
            response.service = message.service
            response.type = MessageType.PlasmaResponse.value

            # If the Plasma object is not initialized, set the error message type to InitialError and add the transaction id
            if not self.initialized:
                response.type = MessageType.InitialError.value

            # Add the error details to the message
            response.data = PlasmaError(
                TXN=message.data.TXN,
                errorCode=ErrorCode(response_data.errorCode),
                localizedMessage=response_data.localizedMessage,
                errorContainer=response_data.errorContainer,
                TID=self.transactionID if not self.initialized else None,
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

    def start_transaction(self, service: PlasmaService, txn: Transaction, data: dict):
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

        loop = asyncio.get_event_loop()
        loop.create_task(send_coroutine)

    async def __send(self, message: Message):
        # Compile the response into bytes
        response_bytes = message.compile()

        # If the response is too big to send in one piece
        if len(response_bytes) > self.fragmentSize:
            # Message is too big, we need to base64 encode it and split it into fragments
            message_bytes = response_bytes[HEADER_LENGTH:]  # Get rid of the header

            # Calculate the size of the message before and after encoding
            decoded_message_size = len(message_bytes)
            message_bytes = b64encode(message_bytes).decode()
            encoded_message_size = len(message_bytes)

            # Split the message into fragments
            fragments = [
                message_bytes[i : i + self.fragmentSize]
                for i in range(0, len(message_bytes), self.fragmentSize)
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
                message_fragment.data = PlasmaChunk(
                    data=fragment,
                    decodedSize=decoded_message_size,
                    size=encoded_message_size,
                )

                # Send the fragment
                await self.ws.send_bytes(message_fragment.compile())
        else:
            # If the response fits into one message, send it
            await self.ws.send_bytes(response_bytes)

    def disconnect(self, reason: int):
        self.start_transaction(
            PlasmaService.ConnectService, Transaction.Goodbye, {"reason": reason}
        )

    def on_disconnect(self):
        """
        Handles the client disconnecting.
        """

        self.timerPing.cancel()
        self.timerMemCheck.cancel()

        if self.accountID:
            self.manager.redis.delete(f"account:{self.accountID}")

            if self.clientType == ClientType.Client:
                self.manager.CLIENTS.pop(self.accountID, None)
            else:
                self.manager.SERVERS.pop(self.accountID, None)

        if self.loginKey:
            self.manager.redis.delete(f"session:{self.loginKey}")

        if self.profileID:
            self.manager.redis.delete(f"profile:{self.profileID}")

        if self.profileLoginKey:
            self.manager.redis.delete(f"persona:{self.profileLoginKey}")

        if self.disconnectReason:
            logger.info(
                msg=f"{self.ws.client.host}:{self.ws.client.port}  -> Disconnected: {self.disconnectReason} ({self.disconnectMessage})"
            )
        else:
            logger.info(
                msg=f"{self.ws.client.host}:{self.ws.client.port}  -> Disconnected"
            )
