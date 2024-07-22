import queue
import secrets
from datetime import datetime
from typing import Tuple

import bcrypt
import mongoengine
from mongoengine import Q, connect
from pydantic import SecretStr
from redis import Redis

from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.database.mongo.documents.Accounts import Accounts
from bfbc2_masterserver.database.mongo.documents.Entitlements import Entitlements
from bfbc2_masterserver.database.mongo.documents.Games import Games
from bfbc2_masterserver.database.mongo.documents.Keys import Keys
from bfbc2_masterserver.database.mongo.documents.Lobbies import Lobbies
from bfbc2_masterserver.database.mongo.documents.Messages import Messages
from bfbc2_masterserver.database.mongo.documents.Personas import Personas
from bfbc2_masterserver.database.mongo.documents.Records import Records
from bfbc2_masterserver.database.mongo.documents.Stats import Stats as StatsDocument
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.messages.plasma.ranking.GetTopNAndStats import Leaderboard
from bfbc2_masterserver.messages.theater.commands.CreateGame import CreateGameRequest
from bfbc2_masterserver.messages.theater.commands.GetGameList import GameData
from bfbc2_masterserver.messages.theater.commands.GetLobbyList import Lobby
from bfbc2_masterserver.messages.theater.commands.UpdateGame import UpdateGameRequest
from bfbc2_masterserver.models.plasma.database.Account import Account
from bfbc2_masterserver.models.plasma.database.Association import Association
from bfbc2_masterserver.models.plasma.database.Entitlement import Entitlement
from bfbc2_masterserver.models.plasma.database.Game import GameServer
from bfbc2_masterserver.models.plasma.database.Message import (
    Attachment,
    Message,
    Target,
)
from bfbc2_masterserver.models.plasma.database.Persona import Persona
from bfbc2_masterserver.models.plasma.database.Record import Record
from bfbc2_masterserver.models.plasma.database.Stats import RankedStat, Stat


class MongoDB(BaseDatabase):

    redis: Redis

    def __init__(self, connection_string: str, redis: Redis):
        super().__init__(connection_string)

        self.redis = redis

        connect(host=connection_string)
        self.prepare_db()

    def register(self, **kwargs) -> bool | ErrorCode:
        if Accounts.objects(nuid=kwargs["nuid"]).first():
            return ErrorCode.ALREADY_REGISTERED

        hashed_password = bcrypt.hashpw(
            kwargs["password"].get_secret_value().encode("utf-8"), bcrypt.gensalt()
        )

        seq_account = self.redis.incr("seq:account")

        account = Accounts(
            id=seq_account,
            nuid=kwargs["nuid"],
            password=hashed_password.decode(),
            globalOptin=kwargs.get("globalOptin", False),
            thirdPartyOptin=kwargs.get("thirdPartyOptin", False),
            parentalEmail=kwargs.get("parentalEmail", None),
            DOBDay=kwargs.get("DOBDay", None),
            DOBMonth=kwargs.get("DOBMonth", None),
            DOBYear=kwargs.get("DOBYear", None),
            zipCode=kwargs.get("zipCode", None),
            country=kwargs.get("country", None),
            language=kwargs.get("language", None),
            tosVersion=kwargs.get("tosVersion", None),
            serviceAccount=kwargs.get("serviceAccount", False),
        ).save()

        return True

    def login(self, **kwargs) -> Account | ErrorCode:
        account = Accounts.objects(nuid=kwargs["nuid"]).first()

        if not account:
            return ErrorCode.USER_NOT_FOUND

        account: Accounts
        password = kwargs["password"]

        if password is None:
            return ErrorCode.INVALID_PASSWORD
        else:
            password = (
                password.get_secret_value()
                if isinstance(password, SecretStr)
                else password
            )

        if not bcrypt.checkpw(
            password.encode("utf-8"),
            account.password.encode("utf-8"),
        ):
            return ErrorCode.INVALID_PASSWORD

        return self.get_account(account.id)

    def get_account(self, account_id) -> Account | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        return Account(
            id=account.id,
            password=account.password,
            nuid=account.nuid,
            globalOptin=account.globalOptin,
            thirdPartyOptin=account.thirdPartyOptin,
            parentalEmail=account.parentalEmail,
            DOBDay=account.DOBDay,
            DOBMonth=account.DOBMonth,
            DOBYear=account.DOBYear,
            zipCode=account.zipCode,
            country=account.country,
            language=account.language,
            tosVersion=account.tosVersion,
            serviceAccount=account.serviceAccount,
        )

    def get_personas(self, account_id) -> list[str]:
        account = Accounts.objects(id=account_id).first()
        personas_list = []

        for persona in account.personas:
            personas_list.append(persona["name"])

        return personas_list

    def add_persona(self, account_id, name) -> bool | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        seq_persona = self.redis.incr("seq:persona")

        persona = Personas(
            id=seq_persona,
            name=name,
        ).save()

        account.personas.append(persona)
        account.save()

        return True

    def disable_persona(self, account_id, name) -> bool | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        # Check if the persona belongs to the account
        if not account:
            return ErrorCode.USER_NOT_FOUND

        for persona in account.personas:
            if persona.name == name:
                Personas(name=name).delete()

        return True

    def get_persona(self, account_id, name) -> Persona | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        personas = account.personas

        for persona in personas:
            if persona.name == name:
                return Persona(id=persona.id, name=persona.name)

        return ErrorCode.USER_NOT_FOUND

    def get_persona_by_id(self, persona_id) -> Persona | ErrorCode:
        persona = Personas.objects(id=persona_id).first()

        if isinstance(persona, Personas) is False:
            return ErrorCode.USER_NOT_FOUND

        return Persona(id=persona.id, name=persona.name)

    def accept_tos(self, account_id, version) -> bool | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        account.tosVersion = version
        account.save()

        return True

    def is_entitled(self, account_id, entitlement_id) -> bool:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return False

        for entitlement in account.entitlements:
            if entitlement.tag == entitlement_id:
                return True

        return False

    def entitle_game(self, account_id, key) -> bool | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        key = Keys.objects(key=key, active=True).first()

        if isinstance(key, Keys) is False:
            return ErrorCode.CODE_NOT_FOUND

        # Add the entitlement to the account
        for target in key.targets:
            entitlement = Entitlements(
                tag=target.tag,
                grant_date=datetime.now(),
                termination_date=None,
                group_name=target.group,
                product_id=target.product,
                version=0,
                is_game_entitlement=target.isGameEntitlement,
            )

            entitlement.save()

            account.entitlements.append(entitlement)
            account.save()

        if key.consumable:
            key.active = False
            key.save()

        return True

    def get_assocation(
        self, persona_id: int, association_type: AssocationType
    ) -> Tuple[str, list[Association]] | ErrorCode:
        persona = Personas.objects(id=persona_id).first()

        if isinstance(persona, Personas) is False:
            return ErrorCode.USER_NOT_FOUND

        match association_type:
            case AssocationType.PlasmaBlock:
                associations = persona.blocked
            case AssocationType.PlasmaFriends:
                associations = persona.friends
            case AssocationType.PlasmaMute:
                associations = persona.muted
            case AssocationType.PlasmaRecentPlayers:
                associations = persona.recent
            case _:
                raise ValueError("Invalid association type")

        associations = [
            Association(
                id=association.id,
                name=association.name,
                type=1,
                created=association.created_at,
                modified=association.updated_at,
            )
            for association in associations
        ]

        return persona.name, associations

    def get_entitlements(
        self, account_id, groupName, entitlementTag
    ) -> list[Entitlement] | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        filtered = []

        for entitlement in account.entitlements:
            # Filter out entitlements
            if entitlement.group_name == groupName or entitlement.tag == entitlementTag:
                filtered.append(entitlement)

        return [
            Entitlement(
                userId=account_id,
                entitlementId=str(entitlement.id),
                entitlementTag=entitlement.tag,
                grantDate=entitlement.grant_date,
                terminationDate=entitlement.termination_date,
                groupName=entitlement.group_name,
                productId=entitlement.product_id,
                version=entitlement.version,
                status="ACTIVE",
            )
            for entitlement in filtered
        ]

    def _add_key(self, data, consumable=True) -> None:
        key = Keys.objects(key=data["key"]).first()

        if key:
            return

        Keys(
            key=data["key"],
            targets=[
                {
                    "tag": target["tag"],
                    "group": target.get("group", None),
                    "product": target.get("product", None),
                    "isGameEntitlement": target.get("isGameEntitlement", False),
                }
                for target in data["targets"]
            ],
            consumable=consumable,
        ).save()

    def entitle_user(self, account_id, key) -> list[Entitlement] | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        key = Keys.objects(key=key, active=True).first()

        if isinstance(key, Keys) is False:
            return ErrorCode.CODE_NOT_FOUND

        entitlements = []

        # Add the entitlement to the account
        for target in key.targets:
            entitlement = Entitlements(
                tag=target.tag,
                grant_date=datetime.now(),
                termination_date=None,
                group_name=target.group,
                product_id=target.product,
                version=0,
                is_game_entitlement=target.isGameEntitlement,
            )

            entitlement.save()
            entitlements.append(entitlement)

            account.entitlements.append(entitlement)
            account.save()

        if key.consumable:
            key.active = False
            key.save()

        return [
            Entitlement(
                userId=account_id,
                entitlementId=str(entitlement.id),
                entitlementTag=entitlement.tag,
                grantDate=entitlement.grant_date,
                terminationDate=entitlement.termination_date,
                groupName=entitlement.group_name,
                productId=entitlement.product_id,
                version=entitlement.version,
                status="ACTIVE",
            )
            for entitlement in entitlements
        ]

    def get_messages(self, persona_id) -> list[Message]:
        # Get messages for the account (look for messages with the account in the receivers list)
        messages_db = Messages.objects(receivers__in=[persona_id]).all()

        messages = [
            Message(
                attachments=[
                    Attachment(
                        key=attachment.key,
                        type=attachment.type,
                        data=attachment.data,
                    )
                    for attachment in message.attachments
                ],
                deliveryType=message.deliveryType,
                messageId=message.messageId,
                messageType=message.messageType,
                purgeStrategy=message.purgeStrategy,
                from_=Target(
                    name=message.sender.name,
                    id=message.sender.id,
                    type=1,
                ),
                to=[
                    Target(
                        name=receiver.name,
                        id=receiver.id,
                        type=1,
                    )
                    for receiver in message.receivers
                ],
                timeSent=message.timeSent,
                expiration=message.expiration,
            )
            for message in messages_db
        ]

        return messages

    def get_stats(self, persona_id, keys) -> list[Stat]:
        statsDoc = StatsDocument.objects(persona_id=persona_id).first()

        if not statsDoc:
            statsDoc = []

        statsDict = dict(statsDoc)

        stats = []

        for key in keys:
            if key not in statsDict:
                continue

            stat = Stat(key=key, value=statsDict[key])
            stats.append(stat)

        return stats

    def get_ranked_stats(self, persona_id, keys) -> list[RankedStat]:
        statsDoc = StatsDocument._get_collection()

        stats = []

        for key in keys:
            pipeline = [
                {
                    "$setWindowFields": {
                        "sortBy": {key: 1},
                        "output": {
                            "rank": {"$rank": {}},
                        },
                    }
                },
                {
                    "$match": {
                        "persona_id": persona_id,
                    }
                },
            ]

            response = statsDoc.aggregate(pipeline)
            response = dict(response)

            if key not in response:
                continue

            stat = RankedStat(
                key=key,
                value=response[key],
                rank=response["rank"],
            )

            stats.append(stat)

        return stats

    def get_leaderboard(self, keys) -> list[Leaderboard]:
        statsDoc = StatsDocument._get_collection()

        leaderboards = []

        for key in keys:
            pipeline = [
                {
                    "$setWindowFields": {
                        "sortBy": {key: 1},
                        "output": {
                            "rank": {"$rank": {}},
                        },
                    }
                },
            ]

            response = statsDoc.aggregate(pipeline)
            response = dict(response)

            if key not in response:
                continue

            leaderboard = Leaderboard(
                addStats=[
                    Stat(
                        key=key,
                        value=response[key],
                    )
                ]
            )

            leaderboards.append(leaderboard)

        return leaderboards

    def get_records(self, persona_id, type) -> list[Record]:
        recordsDoc = Records.objects(persona_id=persona_id, name=type).all()

        records = [
            Record(
                key=record.key,
                value=record.value,
                updated=record.updated,
            )
            for record in recordsDoc
        ]

        return records

    def get_lobbies(self) -> list[Lobby]:
        lobbiesDoc = Lobbies.objects().all()

        lobbies = [
            Lobby.model_validate(
                {
                    "LID": lobby.id,
                    "PASSING": self.get_lobby_games_count(lobby.id),
                    "NAME": lobby.name,
                    "LOCALE": lobby.locale,
                    "MAX-GAMES": lobby.maxGames,
                    "NUM-GAMES": self.get_lobby_games_count(lobby.id),
                }
            )
            for lobby in lobbiesDoc
        ]
        return lobbies

    def _add_lobby(self, name, locale) -> bool | ErrorCode:
        if Lobbies.objects(name=name).first():
            return False

        seq_lobby = self.redis.incr("seq:lobby")

        Lobbies(
            id=seq_lobby,
            name=name,
            locale=locale,
        ).save()

        return True

    def get_lobby_games_count(self, lobby_id) -> int:
        gamesDoc = Games.objects(lid=lobby_id).count()
        return gamesDoc

    def get_lobby_games(self, lobby_id) -> list[GameData]:
        gamesDoc = Games.objects(lid=lobby_id).all()

        games = []

        for game in gamesDoc:
            games.append(
                GameData.model_validate(
                    {
                        "LID": game.lid,
                        "GID": game.id,
                        "N": game.name,
                        "AP": game.activePlayers,
                        "JP": game.joiningPlayers,
                        "QP": game.queuedPlayers,
                        "MP": game.maxPlayers,
                        "F": 0,  # Is Player Favorite
                        "NF": 0,  # Favorite Player Count
                        "HU": 1,
                        "HN": "bfbc2.server.p",
                        "I": game.addrIp,
                        "P": game.addrPort,
                        "J": game.joinMode,
                        "PL": game.platform,
                        "PW": int(0),
                        "V": "2.0",
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
                        "B-U-PunkBusterVersion": None,
                    }
                )
            )

        return games

    def create_game(self, request: CreateGameRequest) -> GameServer:
        # If there's a game with UGID, just return that game if the secret matches
        existingGame = Games.objects(ugid=request.UGID).first()  # type: ignore

        if existingGame:
            if existingGame.secret == request.SECRET.get_secret_value():
                # Refresh ekey
                existingGame.ekey = secrets.token_urlsafe(16)
                existingGame.joinMode = request.JOIN
                existingGame.save()

                return GameServer.model_validate(
                    {
                        "LID": existingGame.lid,
                        "GID": existingGame.id,
                        "MAX-PLAYERS": existingGame.maxPlayers,
                        "EKEY": existingGame.ekey,
                        "UGID": existingGame.ugid,
                        "JOIN": existingGame.joinMode,
                        "SECRET": existingGame.secret,
                        "J": existingGame.joinMode,
                    }
                )

        # Create a new game
        seq_game = self.redis.incr("seq:game")

        game = Games(
            id=seq_game,
            lid=1,
            name=request.NAME.lstrip('"').rstrip('"'),
            addrIp=str(request.INT_IP),
            addrPort=request.INT_PORT,
            platform="PC",
            gameType=request.TYPE,
            queueLength=request.QLEN,
            maxPlayers=request.MAX_PLAYERS,
            maxObservers=request.B_maxObservers,
            numObservers=request.B_numObservers,
            serverHardcore=request.B_U_Hardcore,
            serverHasPassword=request.B_U_HasPassword,
            serverPunkbuster=request.B_U_Punkbuster,
            clientVersion="1.0",
            serverVersion=request.B_version,
            joinMode=request.JOIN,
            ugid=request.UGID,
            ekey=secrets.token_urlsafe(16),
            secret=request.SECRET.get_secret_value(),
        ).save()

        return GameServer.model_validate(
            {
                "LID": game.lid,
                "GID": game.id,
                "MAX-PLAYERS": game.maxPlayers,
                "EKEY": game.ekey,
                "UGID": game.ugid,
                "JOIN": game.joinMode,
                "SECRET": game.secret,
                "J": game.joinMode,
            }
        )

    def update_game(self, request: UpdateGameRequest) -> bool:
        mapping = {
            "N": "name",
            "AP": "activePlayers",
            "JP": "joiningPlayers",
            "QP": "queuedPlayers",
            "MP": "maxPlayers",
            "F": "0",
            "NF": "0",
            "HU": "numObservers",
            "HN": "name",
            "I": "addrIp",
            "P": "addrPort",
            "J": "joinMode",
            "PL": "platform",
            "PW": "serverHasPassword",
            "V": "serverVersion",
            "TYPE": "gameType",
            "B-numObservers": "numObservers",
            "B-maxObservers": "maxObservers",
            "B-version": "serverVersion",
            "B-U-region": "gameRegion",
            "B-U-level": "gameLevel",
            "B-U-elo": "gameElo",
            "B-U-Softcore": "serverSoftcore",
            "B-U-Hardcore": "serverHardcore",
            "B-U-EA": "serverEA",
            "B-U-HasPassword": "serverHasPassword",
            "B-U-public": "gamePublic",
            "B-U-QueueLength": "queueLength",
            "B-U-gameMod": "gameMod",
            "B-U-gamemode": "gameMode",
            "B-U-sguid": "gameSGUID",
            "B-U-Provider": "providerId",
            "B-U-Time": "gameTime",
            "B-U-hash": "gameHash",
            "B-U-Punkbuster": "serverPunkbuster",
            "B-U-PunkBusterVersion": "punkbusterVersion",
        }

        gid = request.GID

        game = Games.objects(id=gid).first()

        if not game:
            return False

        updated_data = request.model_dump()

        for key, value in updated_data.items():
            setattr(game, mapping.get(key, key), value)

        game.save()

        return True
