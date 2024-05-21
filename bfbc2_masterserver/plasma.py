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

    accountID: str | None = None
    profileID: str | None = None
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

        # Log the incoming message
        logger.debug(f"{self.ws.client.host}:{self.ws.client.port} -> {message}")

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
            response = TransactionError(ErrorCode.NOT_INITIALIZED)
        # If the message type is a request, handle the request
        elif message_type in [MessageType.PlasmaRequest, MessageType.PlasmaResponse]:
            response = self.__handle_request(service, message)
        # If the message type is not valid, raise an error
        else:
            raise ValueError(f"Invalid message type: {message_type}")

        # If the response is None, raise an error
        if response is None:
            raise ValueError("Response is None")
        # If the response is a TransactionSkip, return without doing anything
        elif isinstance(response, TransactionSkip):
            return

        # Send the response
        if isinstance(response, TransactionError):
            # Prepare an error message
            error_message = Message()
            error_message.service = (
                service.value if service is not None else message.service
            )
            error_message.type = MessageType.PlasmaResponse.value
            error_message.data["TXN"] = message.data.get("TXN")

            # If the Plasma object is not initialized, set the error message type to InitialError and add the transaction id
            if not self.initialized:
                error_message.type = MessageType.InitialError.value
                error_message.data["TID"] = self.transactionID

            # Add the error details to the message
            error_message.data["errorCode"] = response.errorCode
            error_message.data["localizedMessage"] = response.localizedMessage
            error_message.data["errorContainer"] = response.errorContainer

            # Send the error message
            await self.__send(error_message)
        elif isinstance(response, Message):
            # Prepare the response message
            response.service = service.value
            response.type = MessageType.PlasmaResponse.value
            response.data["TXN"] = message.data.get("TXN")

            # Compile the response into bytes
            response_bytes = response.compile()

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
                    message_fragment.service = service.value
                    message_fragment.type = MessageType.PlasmaChunkedResponse.value

                    # Add the fragment and its size to the message
                    message_fragment.data["data"] = fragment
                    message_fragment.data["decodedSize"] = decoded_message_size
                    message_fragment.data["size"] = encoded_message_size

                    # Send the fragment
                    await self.__send(message_fragment)
            else:
                # If the response fits into one message, send it
                await self.__send(response)

        # Increment the transaction id for the next transaction
        self.transactionID += 1

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
        message_to_send = self.services[service].start_transaction(txn, data)

        if isinstance(message_to_send, TransactionError):
            message = Message()
            message.service = service.value
            message.type = MessageType.PlasmaResponse.value
            message.data["TXN"] = txn
            message.data["errorCode"] = message_to_send.errorCode
            message.data["localizedMessage"] = message_to_send.localizedMessage
            message.data["errorContainer"] = message_to_send.errorContainer

            send_coroutine = self.__send(message, addTransactionID=False)
        else:
            message_to_send.service = service.value
            message_to_send.type = MessageType.PlasmaResponse.value
            message_to_send.data["TXN"] = txn

            send_coroutine = self.__send(message_to_send, addTransactionID=False)

        loop = asyncio.get_event_loop()
        loop.create_task(send_coroutine)

    def __handle_request(self, service: PlasmaService, message: Message):
        return self.services[service].handle(message.data)

    async def __send(self, message: Message, addTransactionID=True):
        # If the message type is not an InitialError, add the transaction ID to the message type
        if message.type != MessageType.InitialError.value and addTransactionID:
            message.type = message.type & 0xFF000000 | self.transactionID

        # Compile the message into bytes and send it to the client
        await self.ws.send_bytes(message.compile())

        # Log the sent message
        logger.debug(f"{self.ws.client.host}:{self.ws.client.port} <- {message}")

    def on_disconnect(self, reason: int | None = None):
        """
        Handles the client disconnecting.
        """

        if reason:
            self.start_transaction(
                PlasmaService.ConnectService, Transaction.Goodbye, {"reason": reason}
            )

            return

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
