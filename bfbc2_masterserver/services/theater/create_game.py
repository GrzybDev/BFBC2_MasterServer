from bfbc2_masterserver.messages.theater.commands.CreateGame import (
    CreateGameRequest,
    CreateGameResponse,
)
from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest, EchoResponse


def handle_create_game(ctx, data: CreateGameRequest):
    database = ctx.manager.database

    gameData = database.create_game(data)

    yield CreateGameResponse.model_validate(
        {
            "LID": gameData.LID,
            "GID": gameData.GID,
            "MAX-PLAYERS": gameData.MAX_PLAYERS,
            "EKEY": gameData.EKEY,
            "UGID": gameData.UGID,
            "JOIN": gameData.JOIN,
            "SECRET": gameData.SECRET,
            "J": gameData.J,
        }
    )
