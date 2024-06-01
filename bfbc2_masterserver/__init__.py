import logging
import sys

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from bfbc2_masterserver.manager import Manager

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# Create FastAPI application
app = FastAPI(title="Battlefield: Bad Company 2 Master Server Emulator")
manager = Manager()

app.mount("/easo", StaticFiles(directory="static"), name="EASO")

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

    await manager.handle_connection(websocket)
