from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.dataclasses.Client import Client
from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.CreateGame import (
    CreateGameRequest,
    CreateGameResponse,
)
from bfbc2_masterserver.models.plasma.database.Game import GameServer


def handle_create_game(ctx: BaseTheaterHandler, data: CreateGameRequest):
    database: BaseDatabase = ctx.manager.database
    gameData: GameServer = database.create_game(ctx.plasma.connection.accountId, data)

    ctx.manager.SERVERS[gameData.GID] = Client()
    ctx.manager.SERVERS[gameData.GID].plasma = ctx.plasma
    ctx.manager.SERVERS[gameData.GID].theater = ctx
    ctx.plasma.connection.gameId = gameData.GID

    yield CreateGameResponse.model_validate(
        {
            "LID": gameData.LID,
            "GID": gameData.GID,
            "MAX-PLAYERS": gameData.maxPlayers,
            "EKEY": gameData.ekey,
            "UGID": gameData.ugid,
            "JOIN": gameData.joinMode,
            "SECRET": gameData.secret,
            "J": gameData.joinMode,
        }
    )
