from ipaddress import ip_address

from django.core.cache import cache

from BFBC2_MasterServer.packet import Packet
from Theater.models import Game, Lobby


async def create_game(connection, message):
    lid = int(message.Get("LID"))
    lobby = await Lobby.objects.get_lobby(lid, connection.locale, connection.plat)

    if ip_address(connection.ip).is_private:
        ip = message.Get("INT-IP")
        port = message.Get("INT-PORT")
    else:
        ip = connection.ip
        port = message.Get("PORT")

    gameObj, gameData = await Game.objects.create_game(
        lobby,
        connection.persona,
        (ip, port),
        str(connection.vers),
        connection.plat,
        message,
    )

    response = Packet()

    for key in gameData:
        response.Set(key, gameData[key])

    connection.gid = gameObj.id
    connection.lid = lid
    cache.set(f"gameSession:{gameData['GID']}", connection.channel_name, timeout=None)

    yield response
