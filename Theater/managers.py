import os
from base64 import b64encode

from asgiref.sync import sync_to_async
from django.db import models
from django.db.models import Q


class LobbyManager(models.Manager):
    @sync_to_async
    def get_lobby(self, lid, locale=None, platform=None):
        if lid == -1:
            lobbyNameBase = f"bfbc2{platform.value}"
            lobbyName = lobbyNameBase
            platformLobbies = self.filter(name__startswith=lobbyName).count()

            if platformLobbies == 0:
                platformLobbies = 1

            lobbyName += "{:02d}".format(platformLobbies)

            from Theater.models import Game

            if Game.objects.filter(lobby__name=lobbyName).count() >= 10000:
                lobbyName = lobbyNameBase + "{:02d}".format(platformLobbies + 1)

            return self.get_or_create(name=lobbyName, locale=locale)[0]
        else:
            return self.get(id=lid)

    @sync_to_async
    def get_lobbies(self):
        from Theater.models import Game

        lobby_data = []

        for lobby in self.all():
            lobby_data.append(
                {
                    "lid": lobby.id,
                    "name": lobby.name,
                    "numGames": Game.objects.filter(lobby=lobby).count(),
                    "locale": lobby.locale,
                    "maxGames": lobby.maxGames,
                }
            )

        return lobby_data


class GameManager(models.Manager):
    @sync_to_async
    def create_game(self, lobby, owner, address, clientVersion, clientPlatform, data):
        secret = data.Get("SECRET")

        game = self.create(
            lobby=lobby,
            owner=owner,
            name=data.Get("NAME").lstrip('"').rstrip('"'),
            addrIp=address[0],
            addrPort=address[1],
            platform=clientPlatform,
            gameType=data.Get("TYPE"),
            queueLength=data.Get("QLEN"),
            maxPlayers=data.Get("MAX-PLAYERS"),
            maxObservers=data.Get("B-maxObservers"),
            numObservers=data.Get("B-numObservers"),
            serverHardcore=data.Get("B-U-Hardcore"),
            serverHasPassword=data.Get("B-U-HasPassword"),
            serverPunkbuster=data.Get("B-U-Punkbuster"),
            clientVersion=clientVersion,
            serverVersion=data.Get("B-version"),
            joinMode=data.Get("JOIN"),
            ugid=data.Get("UGID"),
            ekey=b64encode(os.urandom(16)).decode(),
            secret=secret if len(secret) != 0 else b64encode(os.urandom(64)).decode(),
        )

        return game, {
            "LID": game.lobby.id,
            "GID": game.id,
            "MAX-PLAYERS": game.maxPlayers,
            "EKEY": game.ekey,
            "UGID": game.ugid,
            "JOIN": game.joinMode,
            "SECRET": game.secret,
            "J": game.joinMode,
        }

    @sync_to_async
    def delete_game(self, gid):
        game = self.get(id=gid)
        game.delete()

    @sync_to_async
    def update_game(self, lid, gid, key, value):
        game = self.get(lobby_id=lid, id=gid)
        
        if isinstance(value, str):
            value = value.lstrip('"').rstrip('"')

        match key:
            case "NAME":
                game.name = value
            case "MAX-PLAYERS":
                game.maxPlayers = value
            case "JOIN":
                game.joinMode = value
            case "TYPE":
                game.gameType = value
            case "UGID":
                game.ugid = value
            case "JP":
                game.joiningPlayers = value
            case "QP":
                game.queuedPlayers = value
            case "AP":
                game.activePlayers = value
            case "PL":
                game.platform = value
            case "PW":
                game.isPasswordRequired = value
            case "B-U-level":
                game.gameLevel = value
            case "B-U-QueueLength":
                game.queueLength = value
            case "B-U-Softcore":
                game.serverSoftcore = value
            case "B-U-Hardcore":
                game.serverHardcore = value
            case "B-U-HasPassword":
                game.serverHasPassword = value
            case "B-U-Punkbuster":
                game.serverPunkbuster = value
            case "B-U-PunkbusterVersion":
                game.punkBusterVersion = value
            case "B-U-EA":
                game.serverEA = value
            case "B-U-gameMod":
                game.gameMod = value
            case "B-U-gamemode":
                game.gameMode = value
            case "B-U-Time":
                game.gameTime = value
            case "B-U-region":
                game.gameRegion = value
            case "B-version":
                game.serverVersion = value
            case "B-U-public":
                game.gamePublic = value
            case "B-U-elo":
                game.gameElo = value
            case "B-numObservers":
                game.numObservers = value
            case "B-maxObservers":
                game.maxObservers = value
            case "B-U-sguid":
                game.gameSGUID = value
            case "B-U-hash":
                game.gameHash = value
            case "B-U-Provider":
                game.providerId = value
            case "D-AutoBalance":
                game.gameAutoBalance = value
            case "D-BannerUrl":
                game.gameBannerUrl = value
            case "D-Crosshair":
                game.gameCrosshair = value
            case "D-FriendlyFire":
                game.gameFriendlyFire = value
            case "D-KillCam":
                game.gameKillCam = value
            case "D-Minimap":
                game.gameMinimap = value
            case "D-MinimapSpotting":
                game.gameMinimapSpotting = value
            case "D-ThirdPersonVehicleCameras":
                game.gameThirdPersonVehicleCameras = value
            case "D-ThreeDSpotting":
                game.gameThreeDSpotting = value

        game.save()

    @sync_to_async()
    def find_game(self, gamemode, level):
        gamemodes = gamemode.split("|")

        q = Q(gameMode=gamemodes[0])
        gamemodes.pop(0)

        for gamemode in gamemodes:
            q = q | Q(gameMode=gamemode)

        filtered_games = self.filter(q, serverHasPassword=False).order_by(
            "-serverEA", "-activePlayers"
        )

        if level:
            filtered_games_level = filtered_games.filter(gameLevel=level)

            if filtered_games_level.count() != 0:
                return filtered_games_level.first()

        return filtered_games.first()

    @sync_to_async
    def get_games(self, lobby, gameType, gameMod, count, minGID, **filters):
        filtered_games = self.filter(
            id__gt=int(minGID), lobby=lobby, gameType=gameType, gameMod=gameMod
        )

        if count > 0:
            filtered_games = filtered_games[:count]

        games = []

        for game in filtered_games:
            if filters.get("favGame"):
                serverName = game.name
                favGames = filters.get("favGame").split(";")

                isInFavGame = False
                for favGame in favGames:
                    if favGame.casefold() == serverName.casefold():
                        isInFavGame = True
                        break

                if not isInFavGame:
                    continue

            if filters.get("notFull", False):
                if game.activePlayers >= game.maxPlayers:
                    continue

            if filters.get("minPlayers", 0):
                if game.activePlayers < filters.get("minPlayers"):
                    continue

            if filters.get("gamemode", None):
                if game.gameMode != filters.get("gamemode"):
                    continue

            if filters.get("level", None):
                if game.gameLevel != filters.get("level"):
                    continue

            if filters.get("region", None):
                if game.gameRegion != filters.get("region"):
                    continue

            if filters.get("public", False):
                if not game.gamePublic:
                    continue

            if filters.get("punkbuster", False):
                if not game.serverPunkbuster:
                    continue

            if filters.get("password", False):
                if not game.serverHasPassword:
                    continue

            if filters.get("softcore", False):
                if not game.serverSoftcore:
                    continue

            if filters.get("ea", False):
                if not game.serverEA:
                    continue

            game_data = {
                "LID": game.lobby.id,
                "GID": game.id,
                "N": game.name,
                "AP": game.activePlayers,
                "JP": game.joiningPlayers,
                "QP": game.queuedPlayers,
                "MP": game.maxPlayers,
                "F": 0,  # Is Player Favorite
                "NF": 0,  # Favorite Player Count
                "HU": game.owner.id,
                "HN": game.owner.name,
                "I": game.addrIp,
                "P": game.addrPort,
                "J": game.joinMode,
                "PL": game.platform,
                "PW": int(game.isPasswordRequired),
                "V": game.clientVersion,
                "TYPE": game.gameType,
                "B-numObservers": game.numObservers,
                "B-maxObservers": game.maxObservers,
                "B-version": game.serverVersion,
                "B-U-region": game.gameRegion,
                "B-U-level": game.gameLevel,
                "B-U-elo": game.gameElo,
                "B-U-Softcore": int(game.serverSoftcore),
                "B-U-Hardcore": int(game.serverHardcore),
                "B-U-EA": int(game.serverEA),
                "B-U-HasPassword": int(game.serverHasPassword),
                "B-U-public": int(game.gamePublic),
                "B-U-QueueLength": game.queueLength,
                "B-U-gameMod": game.gameMod,
                "B-U-gamemode": game.gameMode,
                "B-U-sguid": game.gameSGUID,
                "B-U-Provider": game.providerId,
                "B-U-Time": game.gameTime,
                "B-U-hash": game.gameHash,
                "B-U-Punkbuster": int(game.serverPunkbuster),
            }

            if game_data["B-U-Punkbuster"]:
                game_data["B-U-PunkBusterVersion"] = game.punkBusterVersion

            games.append(game_data)

        return games

    @sync_to_async
    def get_lobby_games_count(self, lobby):
        return self.filter(lobby=lobby).count()

    @sync_to_async
    def get_game(self, lobby_id, game_id):
        return self.get(lobby_id=lobby_id, id=game_id)

    @sync_to_async
    def get_game_data(self, lobby_id, game_id):
        game = self.get(lobby_id=lobby_id, id=game_id)

        game_data = {
            "LID": game.lobby.id,
            "GID": game.id,
            "N": game.name,
            "AP": game.activePlayers,
            "JP": game.joiningPlayers,
            "QP": game.queuedPlayers,
            "MP": game.maxPlayers,
            "HU": game.owner.id,
            "HN": game.owner.name,
            "I": game.addrIp,
            "P": game.addrPort,
            "J": game.joinMode,
            "PL": game.platform,
            "PW": int(game.isPasswordRequired),
            "V": game.clientVersion,
            "TYPE": game.gameType,
            "B-numObservers": game.numObservers,
            "B-maxObservers": game.maxObservers,
            "B-version": game.serverVersion,
            "B-U-region": game.gameRegion,
            "B-U-level": game.gameLevel,
            "B-U-elo": game.gameElo,
            "B-U-Softcore": int(game.serverSoftcore),
            "B-U-Hardcore": int(game.serverHardcore),
            "B-U-EA": int(game.serverEA),
            "B-U-HasPassword": int(game.serverHasPassword),
            "B-U-public": int(game.gamePublic),
            "B-U-QueueLength": game.queueLength,
            "B-U-gameMod": game.gameMod,
            "B-U-gamemode": game.gameMode,
            "B-U-sguid": game.gameSGUID,
            "B-U-Provider": game.providerId,
            "B-U-Time": game.gameTime,
            "B-U-hash": game.gameHash,
            "B-U-Punkbuster": int(game.serverPunkbuster),
        }

        return game_data

    @sync_to_async
    def get_game_details(self, lobby_id, game_id):
        from Theater.models import GameDescription, PlayerData

        game = self.get(lobby_id=lobby_id, id=game_id)

        game_details = {
            "LID": game.lobby.id,
            "GID": game.id,
            "D-AutoBalance": int(game.gameAutoBalance),
            "D-Crosshair": int(game.gameCrosshair),
            "D-FriendlyFire": int(game.gameFriendlyFire),
            "D-KillCam": int(game.gameKillCam),
            "D-Minimap": int(game.gameMinimap),
            "D-MinimapSpotting": int(game.gameMinimapSpotting),
            "D-ThirdPersonVehicleCameras": int(game.gameThirdPersonVehicleCameras),
            "D-ThreeDSpotting": int(game.gameThreeDSpotting),
            "UGID": game.ugid,
        }

        serverDescriptions = GameDescription.objects.filter(owner=game)
        game_details["D-ServerDescriptionCount"] = serverDescriptions.count()

        for i, serverDescription in enumerate(serverDescriptions):
            game_details[f"D-ServerDescription{i}"] = serverDescription.text

        if game.gameBannerUrl:
            game_details["D-BannerUrl"] = game.gameBannerUrl

        for i in range(game.maxPlayers):
            pdat = PlayerData.objects.filter(owner=game, index=i + 1).first()

            if game.maxPlayers < 10:
                game_details[f"D-pdat{i}"] = pdat.data
            else:
                game_details[f"D-pdat{i:02}"] = pdat.data

        return game_details

    @sync_to_async
    def get_game_owner(self, lobby_id, game_id):
        return self.get(lobby_id=lobby_id, id=game_id).owner

    @sync_to_async
    def increment_joining_players(self, lobby_id, game_id):
        game = self.get(lobby_id=lobby_id, id=game_id)
        game.joiningPlayers += 1
        game.save()
    
    @sync_to_async
    def decrement_joining_players(self, lobby_id, game_id):
        game = self.get(lobby_id=lobby_id, id=game_id)
        game.joiningPlayers -= 1
        game.save()

    @sync_to_async
    def increment_active_players(self, lobby_id, game_id):
        game = self.get(lobby_id=lobby_id, id=game_id)
        game.activePlayers += 1
        game.save()

    @sync_to_async
    def decrement_active_players(self, lobby_id, game_id):
        game = self.get(lobby_id=lobby_id, id=game_id)
        game.activePlayers -= 1
        game.save()


class PlayerDataManager(models.Manager):
    @sync_to_async
    def update_player_data(self, game, index, pdat):
        game = self.get_or_create(owner=game, index=index + 1)[0]
        game.data = pdat
        game.save()


class GameDescriptionManager(models.Manager):
    @sync_to_async
    def set_game_description_count(self, game, count):
        # Reduce the number of description objects to the new count
        self.filter(owner=game)[count:].delete()

    @sync_to_async
    def set_game_description(self, game, index, text):
        # Get or create the description object
        description = self.get_or_create(owner=game, index=index)[0]
        description.text = text
        description.save()
