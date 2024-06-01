import logging
import sys

from fastapi import FastAPI, HTTPException, Response, WebSocket
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


@app.get("/fileupload/locker2.jsp")
async def locker(site: str, cmd: str, lkey: str, pers: str, game: str):
    # More-or-less original server behaviour
    response = '<?xml version="1.0" encoding="UTF-8"?>'

    if site != "easo" or cmd != "dir":
        raise HTTPException(status_code=500, detail="Invalid command")

    ownr = manager.redis.get(f"persona:{lkey}")

    if not ownr:
        response += '<LOCKER error="2"/>'
        return Response(response, media_type="text/xml")

    if game != "/eagames/BFBC2":
        raise HTTPException(
            status_code=401, detail="This request requires HTTP authentication."
        )

    response += f'<LOCKER error="0" game="{game}" maxBytes="2867200" maxFiles="10" numBytes="0" numFiles="0" ownr="{int(ownr.decode("utf-8"))}" pers="{pers}"/>'  # type: ignore
    return Response(response, media_type="text/xml")


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
