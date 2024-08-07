from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.UpdateGame import UpdateGameRequest


def handle_update_game(ctx: BaseTheaterHandler, data: UpdateGameRequest):
    database = ctx.manager.database
    database.game_update(data)

    yield
