import random
import string

from bfbc2_masterserver.dataclasses.Handler import BaseHandler, BaseTheaterHandler
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.theater.TheaterCommand import TheaterCommand
from bfbc2_masterserver.messages.theater.commands.EnterGame import (
    EnterGameHostRequest,
    EnterGameNotice,
    EnterGameRequest,
    EnterGameResponse,
)


def handle_enter_game(ctx: BaseTheaterHandler, data: EnterGameRequest):
    clientPlasma = ctx.client
    if not clientPlasma.connection.persona:
        return

    pid = ctx.manager.redis.incr(f"pid:{data.GID}")

    try:
        serverClient = ctx.manager.SERVERS[data.GID]
    except KeyError:
        return

    game = ctx.manager.database.game_get(data.LID, data.GID)

    if not game:
        return

    serverFull = False  # TODO: Handle queue
    if serverFull:
        return

    yield EnterGameResponse(LID=data.LID, GID=data.GID, QPOS=None, QLEN=None)

    # Ticket is random 10 digit number, it has to be sent to both client and server
    ticket = "".join(random.choices(string.digits, k=10))

    # Send "Enter Game Host Request" to the game server
    # This is the first step of the handshake

    clientAddr = clientPlasma.plasma.get_client_address()
    if not clientAddr:
        return

    clientIP, _ = clientAddr

    serverClient.theater.start_transaction(
        TheaterCommand.EnterGameHostRequest,
        EnterGameHostRequest.model_validate(
            {
                "R-INT-IP": data.R_INT_IP,
                "R-INT-PORT": data.R_INT_PORT,
                "IP": clientIP,
                "PORT": data.PORT,
                "NAME": clientPlasma.connection.persona.name,
                "PTYPE": data.PTYPE,
                "TICKET": ticket,
                "PID": pid,
                "UID": clientPlasma.connection.persona.id,
                "LID": data.LID,
                "GID": data.GID,
            }
        ),
    )

    if not serverClient.connection.persona:
        return

    serverPersona = ctx.manager.database.persona_get_by_id(
        serverClient.connection.persona.id
    )

    if isinstance(serverPersona, ErrorCode):
        return

    # Send "Enter Game Notice" to the client
    # This is the last step of the handshake and the client will connect to the game server
    serverAddr = serverClient.plasma.get_client_address()
    if not serverAddr:
        return

    serverIP, _ = serverAddr

    ctx.start_transaction(
        TheaterCommand.EnterGameNotice,
        EnterGameNotice.model_validate(
            {
                "PL": clientPlasma.connection.platform,
                "TICKET": ticket,
                "PID": pid,
                "I": serverIP,
                "P": game.addrPort,
                "HUID": serverPersona.id,
                "INT-PORT": game.addrPort,
                "EKEY": game.ekey,
                "INT-IP": game.addrIp,
                "UGID": game.ugid,
                "LID": data.LID,
                "GID": data.GID,
            }
        ),
    )
