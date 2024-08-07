from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.enumerators.theater.TheaterCommand import TheaterCommand
from bfbc2_masterserver.messages.theater.commands.GetGameList import (
    GameData,
    GetGameListRequest,
    GetGameListResponse,
)


def handle_get_game_list(ctx: BaseTheaterHandler, data: GetGameListRequest):
    database = ctx.manager.database

    lobby = database.lobby_get(data.LID)

    if not lobby:
        return

    games = database.lobby_get_games(data)
    games_count = database.lobby_get_games_count(data.LID)

    yield GetGameListResponse.model_validate(
        {
            "LOBBY-NUM-GAMES": games_count,
            "NUM-GAMES": len(games),
            "LID": data.LID,
            "LOBBY-MAX-GAMES": lobby.maxGames,
        }
    )

    for game in games:
        yield GameData.model_validate(
            {
                "LID": game.lobby.id,
                "GID": game.id,
                "N": game.serverName,
                "AP": game.activePlayers,
                "JP": game.joiningPlayers,
                "QP": game.queuedPlayers,
                "MP": game.maxPlayers,
                "F": 0,  # Is player favourite?
                "NF": 0,  # Favourite player count?
                "HU": game.owner.id,
                "HN": game.owner.name,
                "I": game.addrIp,
                "P": game.addrPort,
                "J": game.joinMode,
                "PL": game.platform,
                "PW": game.serverHasPassword,
                "V": game.clientVersion,
                "TYPE": game.gameType,
                "B-numObservers": game.numObservers,
                "B-maxObservers": game.maxObservers,
                "B-version": game.serverVersion,
                "B-U-region": game.gameRegion,
                "B-U-level": game.gameLevel,
                "B-U-elo": game.gameElo,
                "B-U-Softcore": game.serverSoftcore,
                "B-U-Hardcore": game.serverHardcore,
                "B-U-EA": game.serverEA,
                "B-U-HasPassword": game.serverHasPassword,
                "B-U-public": game.gamePublic,
                "B-U-QueueLength": game.queueLength,
                "B-U-gameMod": game.gameMod,
                "B-U-gamemode": game.gameMode,
                "B-U-sguid": game.gameSGUID,
                "B-U-Provider": game.providerId,
                "B-U-Time": game.gameTime,
                "B-U-hash": game.gameHash,
                "B-U-Punkbuster": game.serverPunkbuster,
                "B-U-PunkBusterVersion": game.punkbusterVersion,
            }
        ), TheaterCommand.GameData
