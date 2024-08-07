from bfbc2_masterserver.dataclasses.Client import Client
from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.messages.theater.commands.CreateGame import (
    CreateGameRequest,
    CreateGameResponse,
)
from bfbc2_masterserver.models.theater.database.Game import Game


def handle_create_game(ctx: BaseTheaterHandler, data: CreateGameRequest):
    database = ctx.manager.database

    if (
        ctx.client.connection.platform is None
        or ctx.client.connection.locale is None
        or ctx.client.connection.clientVersion is None
    ):
        raise Exception("Cannot create game without required connection metadata!")

    if ctx.client.connection.persona is None:
        raise Exception("Cannot create game without a persona!")

    gameData = database.game_create(
        ctx.client.connection.persona.id,
        data,
        clientPlatform=ctx.client.connection.platform,
        clientLocale=ctx.client.connection.locale,
        clientVersion=ctx.client.connection.clientVersion,
    )

    if isinstance(gameData, ErrorCode):
        return

    ctx.manager.SERVERS[gameData.id] = ctx.client
    ctx.client.connection.game = gameData

    yield CreateGameResponse.model_validate(
        {
            "LID": gameData.lobbyId,
            "GID": gameData.id,
            "MAX-PLAYERS": gameData.maxPlayers,
            "EKEY": gameData.ekey,
            "UGID": gameData.ugid,
            "JOIN": gameData.joinMode,
            "SECRET": gameData.secret,
            "J": gameData.joinMode,
        }
    )
