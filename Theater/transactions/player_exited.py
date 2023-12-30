from BFBC2_MasterServer.packet import Packet
from Theater.models import Game
from django.core.cache import cache


async def player_exited(connection, message):
    gid = message.Get("GID")
    lid = message.Get("LID")
    pid = message.Get("PID")

    playerSession = cache.get(f"players:{gid}:{pid}")

    await connection.send_remote_message(playerSession, "KICK", {
        "GID": gid,
        "LID": lid,
        "PID": pid
    })
    
    cache.delete(f"players:{gid}:{connection.pid}")
    cache.delete(f"playerData:{gid}:{connection.pid}")

    if pid in connection.connectingPlayers:
        connection.connectingPlayers.remove(pid)
        await Game.objects.decrement_joining_players(lid, gid)
    else:
        await Game.objects.decrement_active_players(lid, gid)

    response = Packet()
    yield response
