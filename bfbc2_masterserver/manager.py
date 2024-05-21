import logging
import os

from fastapi import WebSocketDisconnect
from redis import Redis

from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.enumerators.message.MessageType import MessageType
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.plasma import Plasma

logger = logging.getLogger(__name__)


class Manager:

    CLIENTS = {}
    SERVERS = {}

    database: BaseDatabase
    redis: Redis

    def __init__(self):
        mongodb_connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
        sql_connection_string = os.environ.get("SQL_CONNECTION_STRING")

        if mongodb_connection_string is not None:
            from bfbc2_masterserver.database.mongo.mongo import MongoDB

            self.database = MongoDB(mongodb_connection_string)
        elif sql_connection_string is not None:
            # TODO: Implement SQL database support
            raise NotImplementedError("SQL database support is not implemented yet.")
        else:
            raise ValueError(
                "No database is configured! Check your environment variables."
            )

        self.redis = Redis(
            host=os.environ.get("REDIS_HOST", "localhost"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
        )

    async def handle_connection(self, websocket):
        await websocket.accept()

        if websocket.client:
            host = websocket.client.host
            port = websocket.client.port
        else:
            host = None
            port = None

        logger.info(f"{host}:{port} -> Connected")

        plasma = Plasma(self, websocket)

        try:
            while True:
                message = Message(raw_data=await websocket.receive_bytes())
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
                    pass
                else:
                    raise ValueError("Unknown message type")
        except WebSocketDisconnect:
            pass
        except Exception as e:
            logger.exception(f"{host}:{port} -> {e}", exc_info=True)
            await websocket.close(code=1002, reason=str(e))
        finally:
            # Clean up
            plasma.on_disconnect()
