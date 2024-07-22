from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.CreateGame import (
    CreateGameRequest,
    CreateGameResponse,
)
from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest, EchoResponse
from bfbc2_masterserver.models.plasma.database.Game import GameServer


def handle_create_game(ctx: BaseTheaterHandler, data: CreateGameRequest):
    database: BaseDatabase = ctx.manager.database
    gameData: GameServer = database.create_game(data)

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
