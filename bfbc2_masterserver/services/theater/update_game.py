from bfbc2_masterserver.messages.theater.commands.UpdateGame import UpdateGameRequest


def handle_update_game(ctx, data: UpdateGameRequest):
    print(data)
    database = ctx.manager.database
    database.update_game(data)

    yield
