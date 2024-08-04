import asyncio
import logging

from fastapi import WebSocket
from pydantic import ValidationError

from bfbc2_masterserver.dataclasses.Handler import BaseHandler, BaseTheaterHandler
from bfbc2_masterserver.dataclasses.Manager import BaseManager
from bfbc2_masterserver.enumerators.fesl.MessageType import MessageType
from bfbc2_masterserver.enumerators.theater.TheaterCommand import TheaterCommand
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.messages.theater.commands.Connect import ConnectRequest
from bfbc2_masterserver.messages.theater.commands.CreateGame import CreateGameRequest
from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest
from bfbc2_masterserver.messages.theater.commands.EnterGame import EnterGameRequest
from bfbc2_masterserver.messages.theater.commands.EnterGameResponse import (
    EnterGameHostResponse,
)
from bfbc2_masterserver.messages.theater.commands.GetGameDetails import (
    GetGameDetailsRequest,
)
from bfbc2_masterserver.messages.theater.commands.GetGameList import GetGameListRequest
from bfbc2_masterserver.messages.theater.commands.GetLobbyList import (
    GetLobbyListRequest,
)
from bfbc2_masterserver.messages.theater.commands.Login import LoginRequest
from bfbc2_masterserver.messages.theater.commands.UpdateBracket import (
    UpdateBracketRequest,
)
from bfbc2_masterserver.messages.theater.commands.UpdateGame import UpdateGameRequest
from bfbc2_masterserver.messages.theater.commands.UpdateGameDetails import (
    UpdateGameDetailsRequest,
)
from bfbc2_masterserver.services.theater.connect import handle_connect
from bfbc2_masterserver.services.theater.create_game import handle_create_game
from bfbc2_masterserver.services.theater.echo import handle_echo
from bfbc2_masterserver.services.theater.enter_game import handle_enter_game
from bfbc2_masterserver.services.theater.enter_game_response import (
    handle_enter_game_response,
)
from bfbc2_masterserver.services.theater.get_game_details import handle_get_game_details
from bfbc2_masterserver.services.theater.get_game_list import handle_get_game_list
from bfbc2_masterserver.services.theater.get_lobby_list import handle_get_lobby_list
from bfbc2_masterserver.services.theater.login import handle_login
from bfbc2_masterserver.services.theater.update_bracket import handle_update_bracket
from bfbc2_masterserver.services.theater.update_game import handle_update_game
from bfbc2_masterserver.services.theater.update_game_details import (
    handle_update_game_details,
)

logger = logging.getLogger(__name__)


class Theater(BaseTheaterHandler):

    handlers = {}

    def __init__(self, manager: BaseManager, plasma: BaseHandler, ws: WebSocket):
        self.manager: BaseManager = manager
        self.plasma: BaseHandler = plasma
        self.websocket: WebSocket = ws

        # Register the handlers
        self.handlers[TheaterCommand.Connect] = handle_connect, ConnectRequest
        self.handlers[TheaterCommand.Login] = handle_login, LoginRequest
        self.handlers[TheaterCommand.Echo] = handle_echo, EchoRequest
        self.handlers[TheaterCommand.GetGameDetails] = (
            handle_get_game_details,
            GetGameDetailsRequest,
        )

        self.handlers[TheaterCommand.GetLobbyList] = (
            handle_get_lobby_list,
            GetLobbyListRequest,
        )

        self.handlers[TheaterCommand.GetGameList] = (
            handle_get_game_list,
            GetGameListRequest,
        )

        self.handlers[TheaterCommand.CreateGame] = handle_create_game, CreateGameRequest

        self.handlers[TheaterCommand.UpdateBracket] = (
            handle_update_bracket,
            UpdateBracketRequest,
        )

        self.handlers[TheaterCommand.UpdateGame] = (
            handle_update_game,
            UpdateGameRequest,
        )

        self.handlers[TheaterCommand.UpdateGameDetails] = (
            handle_update_game_details,
            UpdateGameDetailsRequest,
        )

        self.handlers[TheaterCommand.EnterGameRequest] = (
            handle_enter_game,
            EnterGameRequest,
        )

        self.handlers[TheaterCommand.EnterGameHostResponse] = (
            handle_enter_game_response,
            EnterGameHostResponse,
        )

    async def handle_transaction(self, message: Message) -> None:
        try:
            command = TheaterCommand(message.service)
        except ValueError:
            # If the command is not valid, raise an error
            raise ValueError(f"Invalid command: {message.service}")

        tid = message.data["TID"]

        if not self.isInitialized and command == TheaterCommand.Connect:
            self.transactionID = tid
        elif not self.isInitialized:
            raise ValueError("Theater is not initialized")

        try:
            handler, model = self.handlers[command]
            message.data = model.model_validate(message.data)
            logger.debug(f"{self.get_client_address()} -> {message}")
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

                if isinstance(response, tuple):
                    response, command = response
                    message.service = command.value

                message.type = MessageType.TheaterResponse.value

                message.data = response
                message.data.TID = (
                    self.transactionID if command != TheaterCommand.Echo else tid
                )

                await self.__send(message)

                logger.debug(f"{self.get_client_address()} <- {message}")

            if command != TheaterCommand.Echo:
                self.transactionID += 1

    async def __send(self, message: Message) -> None:
        # Compile the response into bytes
        response_bytes = message.compile()
        await self.websocket.send_bytes(response_bytes)
    def start_theater_transaction(self, service: TheaterCommand, data) -> None:
        message = Message()
        message.service = service.value
        message.type = MessageType.TheaterResponse.value
        message.data = data

        send_coroutine = self.__send(message)

        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        loop.create_task(send_coroutine)
