import logging
from base64 import b64encode

from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.message.MessageType import MessageType
from bfbc2_masterserver.enumerators.plasma.PlasmaService import PlasmaService
from bfbc2_masterserver.error import TransactionError, TransactionSkip
from bfbc2_masterserver.message import HEADER_LENGTH, Message
from bfbc2_masterserver.services.plasma.connect import ConnectService

logger = logging.getLogger(__name__)


class Plasma:

    services = {}

    initialized = False

    fragmentSize: int
    transactionID: int

    def __init__(self, ws):
        self.ws = ws

        # Register services
        self.services[PlasmaService.ConnectService] = ConnectService(self)

    async def handle_transaction(self, message: Message, message_type: MessageType):
        logger.debug(f"{self.ws.client.host}:{self.ws.client.port} -> {message}")

        try:
            service = PlasmaService(message.service)
        except ValueError:
            raise ValueError(f"Invalid service: {message.service}")

        tid = message.type & 0x00FFFFFF

        if not self.initialized and service == PlasmaService.ConnectService:
            self.transactionID = tid  # Set the initial transaction id

        if tid != self.transactionID:
            if message_type == MessageType.PlasmaResponse:
                # Simple transactions with a transaction id of 0 are unscheduled transactions (responses)
                # Check if this unscheduled transaction is allowed
                pass
            else:
                raise ValueError(
                    f"Invalid transaction id: {tid} (expected: {self.transactionID})"
                )

        if not self.initialized and message_type != MessageType.PlasmaRequest:
            response = TransactionError(ErrorCode.NOT_INITIALIZED)
        elif message_type == MessageType.PlasmaRequest:
            response = self.handle_request(service, message)
        else:
            raise ValueError(f"Invalid message type: {message_type}")

        if response is None:
            raise ValueError("Response is None")
        elif isinstance(response, TransactionSkip):
            return

        # Send the response
        if isinstance(response, TransactionError):
            error_message = Message()
            error_message.service = (
                service.value if service is not None else message.service
            )
            error_message.type = MessageType.PlasmaResponse.value
            error_message.data["TXN"] = message.data.get("TXN")

            if not self.initialized:
                error_message.type = MessageType.InitialError.value
                error_message.data["TID"] = self.transactionID

            error_message.data["errorCode"] = response.errorCode
            error_message.data["localizedMessage"] = response.localizedMessage
            error_message.data["errorContainer"] = response.errorContainer

            await self.send(error_message)
        elif isinstance(response, Message):
            response.service = service.value
            response.type = MessageType.PlasmaResponse.value
            response.data["TXN"] = message.data.get("TXN")

            response_bytes = response.compile()

            if len(response_bytes) > self.fragmentSize:
                # Message is too big, we need to base64 encode it and split it into fragments
                message_bytes = response_bytes[HEADER_LENGTH:]  # Get rid of the header

                decoded_message_size = len(message_bytes)
                message_bytes = b64encode(message_bytes).decode()
                encoded_message_size = len(message_bytes)

                fragments = [
                    message_bytes[i : i + self.fragmentSize]
                    for i in range(0, len(message_bytes), self.fragmentSize)
                ]

                for fragment in fragments:
                    message_fragment = Message()
                    message_fragment.service = service.value
                    message_fragment.type = MessageType.PlasmaChunkedResponse.value

                    message_fragment.data["data"] = fragment
                    message_fragment.data["decodedSize"] = decoded_message_size
                    message_fragment.data["size"] = encoded_message_size

                    await self.send(message_fragment)
            else:
                await self.send(response)

        self.transactionID += 1

    def handle_request(self, service: PlasmaService, message: Message):
        match service:
            case PlasmaService.ConnectService:
                return self.services[service].handle(message.data)
            case _:
                raise ValueError(f"Unknown service: {service}")

    async def send(self, message: Message):
        if message.type != MessageType.InitialError.value:
            message.type = message.type & 0xFF000000 | self.transactionID

        await self.ws.send_bytes(message.compile())
        logger.debug(f"{self.ws.client.host}:{self.ws.client.port} <- {message}")
