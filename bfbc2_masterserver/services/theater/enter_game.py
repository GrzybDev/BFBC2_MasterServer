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
from bfbc2_masterserver.messages.theater.commands.QueueEntered import (
    QueueEnteredRequest,
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

    serverFull = game.activePlayers + 1 > game.maxPlayers

    qpos, qlen = None, None

    if serverFull:
        queue_data = ctx.manager.redis.get(f"queue:{data.GID}")

        if not queue_data:
            queue_data = ""
        else:
            queue_data = str(queue_data)

        queue = queue_data.split(";")
        queue.append(str(pid))
        queue_data = ";".join(queue)

        ctx.manager.redis.set(f"queue:{str(data.GID)}", queue_data)
        ctx.manager.redis.set(
            f"queuedPlayers:{str(data.GID)}:{str(pid)}",
            f"{clientPlasma.connection.persona.id};{data.R_INT_IP}:{data.R_INT_PORT};{clientPlasma.connection.internalIp}:{data.PORT};{data.PTYPE}",
        )

        qpos = queue.index(str(pid)) - 1
        qlen = len(queue) - 1

    yield EnterGameResponse(LID=data.LID, GID=data.GID, QPOS=qpos, QLEN=qlen)

    # Ticket is random 10 digit number, it has to be sent to both client and server
    ticket = "".join(random.choices(string.digits, k=10))

    # Send "Enter Game Host Request" to the game server
    # This is the first step of the handshake

    clientAddr = clientPlasma.plasma.get_client_address()
    if not clientAddr:
        return

    clientIP, _ = clientAddr

    if not serverFull:
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
    else:
        serverClient.theater.start_transaction(
            TheaterCommand.QueueEntered,
            QueueEnteredRequest.model_validate(
                {
                    "R-INT-IP": data.R_INT_IP,
                    "R-INT-PORT": data.R_INT_PORT,
                    "NAME": clientPlasma.connection.persona.name,
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
