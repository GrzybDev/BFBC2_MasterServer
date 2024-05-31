import logging

from pydantic import ValidationError

from bfbc2_masterserver.enumerators.message.MessageType import MessageType
from bfbc2_masterserver.enumerators.theater.TheaterCommand import TheaterCommand
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.messages.theater.commands.Connect import ConnectRequest
from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest
from bfbc2_masterserver.messages.theater.commands.Login import LoginRequest
from bfbc2_masterserver.services.theater.connect import handle_connect
from bfbc2_masterserver.services.theater.echo import handle_echo
from bfbc2_masterserver.services.theater.login import handle_login

logger = logging.getLogger(__name__)


class Theater:

    initialized = False
    transactionID = None

    handlers = {}

    def __init__(self, manager, plasma, ws) -> None:
        self.manager = manager
        self.plasma = plasma
        self.ws = ws

        # Register the handlers
        self.handlers[TheaterCommand.Connect] = handle_connect, ConnectRequest
        self.handlers[TheaterCommand.Login] = handle_login, LoginRequest
        self.handlers[TheaterCommand.Echo] = handle_echo, EchoRequest

    async def handle_transaction(self, message: Message):
        try:
            command = TheaterCommand(message.service)
        except ValueError:
            # If the command is not valid, raise an error
            raise ValueError(f"Invalid command: {message.service}")

        tid = message.data["TID"]

        if not self.initialized and command == TheaterCommand.Connect:
            self.transactionID = tid
        elif not self.initialized:
            raise ValueError("Theater is not initialized")

        try:
            handler, model = self.handlers[command]
            message.data = model.model_validate(message.data)
            logger.debug(
                f"{self.plasma.ws.client.host}:{self.plasma.ws.client.port} -> {message}"
            )
            responses = handler(self, message.data)
        except ValidationError as e:
            raise ValueError(f"Invalid message: {e}")
        except KeyError:
            raise ValueError(f"Command not implemented: {command}")
        except Exception as e:
            raise ValueError(f"Error handling message: {e}")

        if responses is not None and self.transactionID:
            for response in responses:
                if response is None:
                    continue

                message.type = MessageType.TheaterResponse.value

                message.data = response
                message.data.TID = (
                    self.transactionID if command != TheaterCommand.Echo else tid
                )

                await self.__send(message)

                logger.debug(
                    f"{self.plasma.ws.client.host}:{self.plasma.ws.client.port} <- {message}"
                )

            if command != TheaterCommand.Echo:
                self.transactionID += 1

    async def __send(self, message: Message):
        # Compile the response into bytes
        response_bytes = message.compile()
        await self.ws.send_bytes(response_bytes)
