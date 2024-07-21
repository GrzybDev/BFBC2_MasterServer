from bfbc2_masterserver.messages.theater.commands.UpdateGameDetails import (
    UpdateGameDetailsRequest,
)


def handle_update_game_details(ctx, data: UpdateGameDetailsRequest):
    database = ctx.manager.database
    database.update_game(data)

    yield
