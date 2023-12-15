from Theater.models import Game


async def update_game_data(connection, message):
    keys = message.GetKeys()

    for key in keys:
        await Game.objects.update_game(connection.gid, key, message.Get(key))

    yield
