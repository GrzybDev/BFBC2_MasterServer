from BFBC2_MasterServer.packet import Packet
from Theater.models import Game


async def player_entered(connection, message):
    lid = message.Get("LID")
    gid = message.Get("GID")
    pid = message.Get("PID")
    
    connection.connectingPlayers.remove(pid)
    await Game.objects.decrement_joining_players(lid, gid)
    await Game.objects.increment_active_players(lid, gid)

    response = Packet()
    response.Set("PID", pid)

    yield response
