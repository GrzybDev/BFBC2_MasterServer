from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.UpdateGameDetails import (
    UpdateGameDetailsRequest,
)


def handle_update_game_details(ctx: BaseTheaterHandler, data: UpdateGameDetailsRequest):
    database = ctx.manager.database
    database.update_game(data)

    yield
