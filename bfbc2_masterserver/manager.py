import logging
import os

from fastapi import WebSocket, WebSocketDisconnect
from redis import Redis

from bfbc2_masterserver.dataclasses.Manager import BaseManager
from bfbc2_masterserver.enumerators.fesl.MessageType import MessageType
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.plasma import Plasma
from bfbc2_masterserver.theater import Theater

logger = logging.getLogger(__name__)


class Manager(BaseManager):

    def __init__(self):
        mongodb_connection_string: str | None = os.environ.get(
            "MONGODB_CONNECTION_STRING"
        )
        sql_connection_string: str | None = os.environ.get("SQL_CONNECTION_STRING")

        self.redis = Redis(
            host=os.environ.get("REDIS_HOST", "localhost"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
        )

        if mongodb_connection_string is not None:
            from bfbc2_masterserver.database.mongo.mongo import MongoDB

            self.database = MongoDB(mongodb_connection_string, self.redis)
        elif sql_connection_string is not None:
            # TODO: Implement SQL database support
            raise NotImplementedError("SQL database support is not implemented yet.")
        else:
            raise ValueError(
                "No database is configured! Check your environment variables."
            )

    async def handle_connection(self, websocket: WebSocket) -> None:
        await websocket.accept()

        if not websocket.client:
            raise ValueError("Client information is missing")

        address: tuple[str, int] = (websocket.client.host, websocket.client.port)
        logger.info(f"{address} -> Connected")

        plasma = Plasma(self, websocket)
        theater = Theater(self, plasma, websocket)

        try:
            while True:
                raw_data = await websocket.receive_bytes()

                if raw_data.startswith(b"META"):
                    # META messages are workaround for getting the client's internal IP and port
                    remote_info = raw_data.decode("utf-8").split("|")
                    ip, port = remote_info[1], int(remote_info[2])
                    plasma.connection.internalIp = ip
                    plasma.connection.internalPort = port
                    continue

                message = Message(raw_data=raw_data)
                messages: list[bytes] = []

                if message.fragmented:
                    # If the message is fragmented, split it into individual messages

                    while raw_data:
                        message = Message(raw_data=raw_data)
                        messages.append(raw_data[: message.length])
                        raw_data: bytes = raw_data[message.length :]
                else:
                    messages.append(raw_data)

                for raw_message in messages:
                    message = Message(raw_data=raw_message)
                    message_type = MessageType(message.type & 0xFF000000)

                    if message_type in [
                        MessageType.PlasmaRequest,
                        MessageType.PlasmaResponse,
                    ]:
                        await plasma.handle_transaction(message, message_type)
                    elif message_type in [
                        MessageType.TheaterRequest,
                        MessageType.TheaterResponse,
                    ]:
                        await theater.handle_transaction(message)
                    else:
                        raise ValueError("Unknown message type")
        except WebSocketDisconnect:
            pass
        except Exception as e:
            logger.exception(f"{address} -> {e}", exc_info=True)
            await websocket.close(code=1002, reason=str(e))
        finally:
            # Clean up
            plasma.on_disconnect(reason="Connection closed", message=None)
