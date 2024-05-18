import logging
import sys

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from bfbc2_masterserver.enumerators.message.MessageFrom import MessageFrom
from bfbc2_masterserver.enumerators.message.MessageType import MessageType
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.plasma import Plasma

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# Create FastAPI application
app = FastAPI(title="Battlefield: Bad Company 2 Master Server Emulator")


# Define WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    This is a WebSocket endpoint for the FastAPI application.

    This function accepts WebSocket connections, logs the client's host and port, creates a Plasma and Theater instances, and handles messages in a loop until the client disconnects or an exception occurs.

    Args:
        websocket (WebSocket): The WebSocket connection.

    Raises:
        WebSocketDisconnect: If the client disconnects.
        Exception: If any other exception occurs.
    """

    await websocket.accept()

    # Get client's host and port if available
    if websocket.client:
        host = websocket.client.host
        port = websocket.client.port
    else:
        host = None
        port = None

    logger.info(f"{host}:{port} -> Connected")

    # Create Plasma instance
    plasma = Plasma(websocket)

    # Main loop for handling messages
    while True:
        try:
            # Receive and parse message
            message = Message(raw_data=await websocket.receive_bytes())
            message_type = MessageType(message.type & 0xFF000000)

            # Determine message source
            if message_type in [MessageType.PlasmaRequest, MessageType.PlasmaResponse]:
                message_from = MessageFrom.Plasma
            elif False:  # TODO: Add Theater message types
                message_from = MessageFrom.Theater
            else:
                raise ValueError("Unknown message type")

            if message_from == MessageFrom.Plasma:
                # Handle Plasma messages
                await plasma.handle_transaction(message, message_type)
            else:
                # Handle Theater messages
                pass
        except WebSocketDisconnect:
            # Break the loop if client disconnects
            break
        except Exception as e:
            # Log any exceptions and close the connection
            logger.error(f"{host}:{port} -> {e}")
            await websocket.close(code=1002, reason=str(e))
            break

    plasma.on_disconnect()

    if plasma.disconnectReason:
        logger.info(
            msg=f"{host}:{port} -> Disconnected: {plasma.disconnectReason} ({plasma.disconnectMessage})"
        )
    else:
        logger.info(msg=f"{host}:{port} -> Disconnected")
