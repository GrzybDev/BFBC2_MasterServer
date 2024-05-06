import logging
import sys

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from bfbc2_masterserver.enumerators.message.MessageFrom import MessageFrom
from bfbc2_masterserver.enumerators.message.MessageType import MessageType
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.plasma import Plasma

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

app = FastAPI(title="Battlefield: Bad Company 2 Master Server Emulator")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    if websocket.client:
        host = websocket.client.host
        port = websocket.client.port
    else:
        host = None
        port = None

    logger.info(f"{host}:{port} -> Connected")

    plasma = Plasma(websocket)

    while True:
        try:
            message = Message(raw_data=await websocket.receive_bytes())
            message_type = MessageType(message.type & 0xFF000000)

            if message_type == MessageType.PlasmaRequest:
                message_from = MessageFrom.Plasma
            else:
                message_from = MessageFrom.Theater

            if message_from == MessageFrom.Plasma:
                # Handle Plasma messages
                await plasma.handle_transaction(message, message_type)
        except WebSocketDisconnect:
            break
        except Exception as e:
            logger.error(f"{host}:{port} -> {e}")
            await websocket.close(code=1002, reason=str(e))
            break

    logger.info(msg=f"{host}:{port} -> Disconnected")
