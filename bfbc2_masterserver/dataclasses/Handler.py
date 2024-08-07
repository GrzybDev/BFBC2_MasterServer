import asyncio
from abc import abstractmethod

from fastapi import WebSocket

from bfbc2_masterserver.dataclasses.Client import Client
from bfbc2_masterserver.dataclasses.Connection import BaseConnection
from bfbc2_masterserver.dataclasses.Manager import BaseManager
from bfbc2_masterserver.enumerators.fesl.FESLService import FESLService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.enumerators.fesl.MessageType import MessageType
from bfbc2_masterserver.enumerators.theater.TheaterCommand import TheaterCommand
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class BaseHandler:
    client: Client
    manager: BaseManager
    websocket: WebSocket

    transactionID: int = 0

    def get_client_address(self) -> tuple[str, int] | None:
        if not self.websocket.client:
            return None

        return (self.websocket.client.host, self.websocket.client.port)


class BasePlasmaHandler(BaseHandler):
    timerMemCheck: asyncio.TimerHandle | None = None
    timerPing: asyncio.TimerHandle | None = None

    @abstractmethod
    async def handle_transaction(
        self, message: Message, message_type: MessageType
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def start_transaction(
        self, service: FESLService, txn: FESLTransaction, data: PlasmaTransaction
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self, reason: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def on_disconnect(self, reason: int | str, message: str | None) -> None:
        raise NotImplementedError()


class BaseTheaterHandler(BaseHandler):
    isInitialized: bool = False
    updateInProgress: bool = False

    @abstractmethod
    async def handle_transaction(self, message: Message) -> None:
        raise NotImplementedError()

    @abstractmethod
    def start_transaction(
        self, service: TheaterCommand, data: TheaterTransaction
    ) -> None:
        raise NotImplementedError()
