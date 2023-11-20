import random
import string

from django.core.cache import cache

from BFBC2_MasterServer.packet import Packet
from Theater.models import Game


async def enter_game_request(connection, message):
    lid = message.Get("LID")
    gid = message.Get("GID")

    game = await Game.objects.get_game(lid, gid)

    if not game:
        return

    # pid is the unique player id on the game server
    pid = cache.get_or_set(f"nextServerPlayerID:{gid}", 0, timeout=None)
    connection.pid = pid

    cache.incr(f"nextServerPlayerID:{gid}")
    cache.set(f"players:{gid}:{pid}", connection.lkey, timeout=None)

    response = Packet()
    response.Set("LID", lid)
    response.Set("GID", gid)

    serverFull = game.activePlayers + 1 > game.maxPlayers

    if serverFull:
        response.kind = 0x71756575

        queue_str = cache.get_or_set(f"queue:{gid}", "", timeout=None)
        queue_list = queue_str.split(";")
        queue_list.append(str(pid))
        queue_str = ";".join(queue_list)
        cache.set(f"queue:{gid}", queue_str, timeout=None)
        cache.set(
            f"playerData:{gid}:{pid}",
            f"{connection.persona.id};{message.Get('R-INT-IP')}:{message.Get('R-INT-PORT')};{connection.ip}:{message.Get('PORT')};{message.Get('PTYPE')}",
            timeout=None,
        )

        response.Set("QPOS", queue_list.index(str(pid)) - 1)
        response.Set("QLEN", len(queue_list) - 1)

    yield response

    # Ticket is random 10 digit number, it has to be sent to both client and server
    ticket = "".join(random.choices(string.digits, k=10))

    # Sent "Enter Game Host Request" to the game server
    if not serverFull:
        enterGameHostRequestData = {
            "R-INT-IP": message.Get("R-INT-IP"),
            "R-INT-PORT": message.Get("R-INT-PORT"),
            "IP": connection.ip,
            "PORT": message.Get("PORT"),
            "NAME": connection.persona.name,
            "PTYPE": message.Get("PTYPE"),
            "TICKET": ticket,
            "PID": pid,
            "UID": connection.persona.id,
            "LID": lid,
            "GID": gid,
        }

        await connection.send_remote_message_server(
            gid, "EGRQ", enterGameHostRequestData
        )
    else:
        queueEnter = {
            "R-INT-IP": message.Get("R-INT-IP"),
            "R-INT-PORT": message.Get("R-INT-PORT"),
            "NAME": connection.persona.name,
            "PID": pid,
            "UID": connection.persona.id,
            "LID": lid,
            "GID": gid,
        }

        await connection.send_remote_message_server(gid, "QENT", queueEnter)

    owner = await Game.objects.get_game_owner(lid, gid)

    enterGameNotice = Packet(service="EGEG")
    enterGameNotice.Set("PL", connection.plat.value)
    enterGameNotice.Set("TICKET", ticket)
    enterGameNotice.Set("PID", pid)
    enterGameNotice.Set("I", game.addrIp)
    enterGameNotice.Set("P", game.addrPort)
    enterGameNotice.Set("HUID", owner.id)
    enterGameNotice.Set("INT-PORT", game.addrPort)
    enterGameNotice.Set("EKEY", game.ekey)
    enterGameNotice.Set("INT-IP", game.addrIp)
    enterGameNotice.Set("UGID", game.ugid)
    enterGameNotice.Set("LID", lid)
    enterGameNotice.Set("GID", gid)

    if not serverFull:
        yield enterGameNotice
