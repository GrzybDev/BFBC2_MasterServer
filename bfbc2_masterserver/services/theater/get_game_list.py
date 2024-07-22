from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.enumerators.theater.TheaterCommand import TheaterCommand
from bfbc2_masterserver.messages.theater.commands.GetGameList import (
    GetGameListRequest,
    GetGameListResponse,
)


def handle_get_game_list(ctx: BaseTheaterHandler, data: GetGameListRequest):
    database = ctx.manager.database

    games = database.get_lobby_games(data.LID)

    yield GetGameListResponse.model_validate(
        {
            "LOBBY-NUM-GAMES": len(games),
            "NUM-GAMES": len(games) if not data.GID else 0,
            "LID": data.LID,
            "LOBBY-MAX-GAMES": 10000,
        }
    )

    if not data.GID:
        for game in games:
            yield game, TheaterCommand.GameData
