import logging
import os

from fastapi import WebSocket
from redis import Redis
from sqlalchemy import create_engine

from bfbc2_masterserver.database import DatabaseAPI
from bfbc2_masterserver.dataclasses.Client import Client
from bfbc2_masterserver.dataclasses.Connection import BaseConnection
from bfbc2_masterserver.dataclasses.Manager import BaseManager
from bfbc2_masterserver.enumerators.fesl.MessageType import MessageType
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.plasma import Plasma
from bfbc2_masterserver.theater import Theater

logger = logging.getLogger(__name__)


class Manager(BaseManager):

    def __init__(self):
        db_connection_string: str = os.environ.get(
            "DB_CONNECTION_STRING", "sqlite:///db.sqlite3"
        )
        database_engine = create_engine(db_connection_string)
        self.database = DatabaseAPI(database_engine)

        self.redis = Redis(
            os.environ.get("REDIS_HOST", "localhost"),
            int(os.environ.get("REDIS_PORT", 6379)),
        )

    async def connect(self, websocket: WebSocket) -> Client:
        await websocket.accept()

        if not websocket.client:
            raise ValueError("Client information is missing")

        logger.info(f"{websocket.client} -> Connected")

        client = Client()
        client.connection = BaseConnection()
        client.plasma = Plasma(manager=self, client=client, ws=websocket)
        client.theater = Theater(manager=self, client=client, ws=websocket)

        return client

    async def disconnect(self, websocket: WebSocket) -> None:
        if not websocket.client:
            raise ValueError("Client information is missing")

        logger.info(f"{websocket.client} -> Disconnected")

    async def handle_message(self, client: Client, raw_data: bytes) -> None:
        if raw_data.startswith(b"META"):
            # META messages are workaround for getting the client's internal IP and port
            remote_info = raw_data.decode("utf-8").split("|")
            ip, port = remote_info[1], int(remote_info[2])
            client.connection.internalIp = ip
            client.connection.internalPort = port
            return

        message = Message(raw_data=raw_data)
        messages: list[bytes] = []

        if message.fragmented:
            # If the message is fragmented, split it into individual messages

            while raw_data:
                message = Message(raw_data=raw_data)
                messages.append(raw_data[: message.length])
                raw_data = raw_data[message.length :]
        else:
            messages.append(raw_data)

        for raw_message in messages:
            message = Message(raw_data=raw_message)
            message_type = MessageType(message.type & 0xFF000000)

            if message_type in [
                MessageType.PlasmaRequest,
                MessageType.PlasmaResponse,
                MessageType.PlasmaChunkedRequest,
                MessageType.PlasmaChunkedResponse,
            ]:
                await client.plasma.handle_transaction(message, message_type)
            elif message_type in [
                MessageType.TheaterRequest,
                MessageType.TheaterResponse,
            ]:
                await client.theater.handle_transaction(message)
            else:
                raise ValueError("Unknown message type", hex(message.type))
