from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.enumerators.theater.TheaterCommand import TheaterCommand
from bfbc2_masterserver.messages.theater.commands.GetLobbyList import (
    GetLobbyListRequest,
    GetLobbyListResponse,
)


def handle_get_lobby_list(ctx: BaseTheaterHandler, data: GetLobbyListRequest):
    database = ctx.manager.database

    lobbies = database.get_lobbies()
    yield GetLobbyListResponse.model_validate({"NUM-LOBBIES": len(lobbies)})

    for lobby in lobbies:
        yield lobby, TheaterCommand.LobbyData
