from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.enumerators.theater.TheaterCommand import TheaterCommand
from bfbc2_masterserver.messages.theater.commands.GetLobbyList import (
    GetLobbyListRequest,
    GetLobbyListResponse,
    LobbyData,
)


def handle_get_lobby_list(ctx: BaseTheaterHandler, data: GetLobbyListRequest):
    database = ctx.manager.database

    lobbies = database.lobby_get_all()
    yield GetLobbyListResponse.model_validate({"NUM-LOBBIES": len(lobbies)})

    for lobby in lobbies:
        games_count = database.lobby_get_games_count(lobby.id)

        lobby_data = LobbyData.model_validate(
            {
                "LID": lobby.id,
                "PASSING": games_count,
                "NAME": lobby.name,
                "LOCALE": lobby.locale,
                "MAX-GAMES": lobby.maxGames,
                "NUM-GAMES": games_count,
            }
        )

        yield lobby_data, TheaterCommand.LobbyData
