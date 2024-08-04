import asyncio
from abc import abstractmethod
from turtle import update

from fastapi import WebSocket

from bfbc2_masterserver.dataclasses.Connection import BaseConnection
from bfbc2_masterserver.dataclasses.Manager import BaseManager
from bfbc2_masterserver.enumerators.fesl.FESLService import FESLService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.enumerators.theater.TheaterCommand import TheaterCommand
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class BaseHandler:
    connection: BaseConnection

    manager: BaseManager
    websocket: WebSocket

    transactionID: int

    timerMemCheck: asyncio.TimerHandle
    timerPing: asyncio.TimerHandle

    def get_client_address(self) -> str | None:
        if not self.websocket.client:
            return None

        return f"{self.websocket.client.host}:{self.websocket.client.port}"

    @abstractmethod
    def start_transaction(
        self, service: FESLService, txn: FESLTransaction, data: PlasmaTransaction
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def finish_message(
        self, message: Message, response_data, noTransactionID=False
    ) -> Message:
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

    plasma: BaseHandler

    @abstractmethod
    def start_theater_transaction(
        self, service: TheaterCommand, data: TheaterTransaction
    ) -> None:
        raise NotImplementedError()
