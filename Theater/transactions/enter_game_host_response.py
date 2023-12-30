from BFBC2_MasterServer.packet import Packet
from Theater.models import Game


async def enter_game_host_response(connection, message):
    lid = message.Get("LID")
    gid = message.Get("GID")
    pid = message.Get("PID")

    isAllowed = message.Get("ALLOWED")

    if isAllowed:
        # Update player count on server
        connection.connectingPlayers.append(pid)
        await Game.objects.increment_joining_players(lid, gid)

    yield Packet()
