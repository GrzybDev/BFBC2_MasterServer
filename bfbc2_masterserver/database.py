import os
import secrets
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uu import Error

import bcrypt
from sqlalchemy import Engine, func
from sqlmodel import Session, SQLModel, or_, select

from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale
from bfbc2_masterserver.enumerators.client.ClientPlatform import ClientPlatform
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.enumerators.plasma.RecordName import RecordName
from bfbc2_masterserver.enumerators.plasma.StatUpdateType import StatUpdateType
from bfbc2_masterserver.enumerators.theater.GameType import GameType
from bfbc2_masterserver.enumerators.theater.JoinMode import JoinMode
from bfbc2_masterserver.messages.plasma.account.NuGrantEntitlement import (
    NuGrantEntitlementRequest,
)
from bfbc2_masterserver.messages.theater.commands.CreateGame import CreateGameRequest
from bfbc2_masterserver.messages.theater.commands.GetGameList import GetGameListRequest
from bfbc2_masterserver.messages.theater.commands.UpdateGame import UpdateGameRequest
from bfbc2_masterserver.messages.theater.commands.UpdateGameDetails import (
    UpdateGameDetailsRequest,
)
from bfbc2_masterserver.models.plasma.database.Account import Account
from bfbc2_masterserver.models.plasma.database.Association import Association
from bfbc2_masterserver.models.plasma.database.Entitlement import Entitlement
from bfbc2_masterserver.models.plasma.database.Message import Message
from bfbc2_masterserver.models.plasma.database.MessageAttachment import (
    MessageAttachment,
)
from bfbc2_masterserver.models.plasma.database.Persona import Persona
from bfbc2_masterserver.models.plasma.database.Ranking import Ranking
from bfbc2_masterserver.models.plasma.database.Record import Record
from bfbc2_masterserver.models.plasma.database.SerialKey import SerialKey
from bfbc2_masterserver.models.plasma.database.SerialKeyTarget import SerialKeyTarget
from bfbc2_masterserver.models.theater.database.Game import Game
from bfbc2_masterserver.models.theater.database.Lobby import Lobby


class DatabaseAPI:

    _engine: Engine

    _secret_key = os.environ.get("SECRET_KEY", "bfbc2emu")
    _algorithm = os.environ.get("ALGORITHM_OVERRIDE", "HS256")

    __service_accounts = [
        ("bfbc2.server.pc@ea.com", "Che6rEPA"),  # PC Server
        ("bfbc.server.ps3@ea.com", "zAmeH7bR"),  # PS3 Server
        ("bfbc.server.xenon@ea.com", "B8ApRavE"),  # Xbox 360 Server
    ]

    __system_keys = [
        {
            "key": "ACTIVATE-GAME",
            "targets": [
                {"tag": "bfbc2-pc", "isGameEntitlement": True},
                {"tag": "ONLINE_ACCESS", "product": "DR:156691300"},
                {"tag": "BETA_ONLINE_ACCESS", "product": "OFB-BFBC:19121"},
            ],
        },
        {
            "key": "ACTIVATE-VIETNAM",
            "targets": [
                {
                    "tag": "BFBC2:PC:VIETNAM_ACCESS",
                    "group": "BFBC2PC",
                    "product": "DR:219316800",
                },
                {
                    "tag": "BFBC2:PC:VIETNAM_PDLC",
                    "group": "BFBC2PC",
                    "product": "DR:219316800",
                },
            ],
        },
        {
            "key": "ACTIVATE-SPECACT",
            "targets": [
                {
                    "tag": "BFBC2:PC:ALLKIT",
                    "group": "BFBC2PC",
                },
                {
                    "tag": "BFBC2:PC:MAXALLKIT",
                    "group": "BFBC2PC",
                },
            ],
        },
        {
            "key": "ACTIVATE-PREMIUM",
            "targets": [
                {
                    "tag": "BFBC2:PC:LimitedEdition",
                    "group": "BFBC2PC",
                    "product": "OFB-BFBC:19120",
                },
            ],
        },
        {
            "key": "ACTIVATE-VETERAN",
            "targets": [
                {
                    "tag": "BFBC2:PC:ADDSVETRANK",
                    "group": "AddsVetRank",
                    "product": "OFB-EAST:40873",
                },
                {
                    "tag": "BF3:PC:ADDSVETRANK",
                    "group": "AddsVetRank",
                    "product": "OFB-EAST:40873",
                },
            ],
        },
    ]

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

        SQLModel.metadata.create_all(engine)

        # Create service accounts if they don't exist
        for account in self.__service_accounts:
            self.account_register(
                Account(nuid=account[0], password=account[1], serviceAccount=True)
            )

        # Create system keys if they don't exist
        with Session(self._engine) as session:
            for key in self.__system_keys:
                serial_key_query = select(SerialKey).where(SerialKey.key == key["key"])
                existing_key = session.exec(serial_key_query).one_or_none()

                if existing_key:
                    continue

                targets = key["targets"]

                db_targets = []

                for target in targets:
                    serial_key_target = SerialKeyTarget(
                        tag=target["tag"],
                        groupName=target.get("group", None),
                        productId=target.get("product", None),
                        version=target.get("version", 0),
                    )

                    session.add(serial_key_target)
                    session.commit()

                    db_targets.append(serial_key_target)

                serial_key = SerialKey(
                    key=key["key"], reusable=True, used=False, targets=db_targets
                )

                session.add(serial_key)
                session.commit()

        with Session(self._engine) as session:
            # Mark every game as closed (at this stage noone is connected)
            games_query = select(Game)
            games = session.exec(games_query).all()

            for game in games:
                game.joinMode = JoinMode.CLOSED
                session.add(game)

            session.commit()

    def account_register(self, account: Account) -> bool:
        with Session(self._engine) as session:
            # Check if the account already exists
            account_query = select(Account).where(Account.nuid == account.nuid)
            existing_account = session.exec(account_query).one_or_none()

            if existing_account:
                return False

            hashed_password = bcrypt.hashpw(
                account.password.encode("utf-8"), bcrypt.gensalt()
            )
            account.password = hashed_password.decode("utf-8")

            session.add(account)
            session.commit()

            return True

    def account_login(self, nuid: str, password: str) -> Account | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.nuid == nuid)
            account = session.exec(account_query).one_or_none()

            if not account:
                return ErrorCode.USER_NOT_FOUND

            if not bcrypt.checkpw(
                password.encode("utf-8"), account.password.encode("utf-8")
            ):
                return ErrorCode.INVALID_PASSWORD

            return account

    def account_accept_tos(
        self, account_id: int, tos_version: str
    ) -> Account | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.id == account_id)
            account = session.exec(account_query).one_or_none()

            if not account:
                return ErrorCode.USER_NOT_FOUND

            account.tosVersion = tos_version

            session.add(account)
            session.commit()

            return account

    def account_is_entitled(
        self, account_id: int, entitlement_tag: str
    ) -> bool | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.id == account_id)
            account = session.exec(account_query).one_or_none()

            if not account:
                return ErrorCode.USER_NOT_FOUND

            for entitlement in account.entitlements:
                if entitlement.tag == entitlement_tag:
                    return True

            return False

    def account_get_entitlements(
        self, account_id: int, groupName=None, entitlementTag=None
    ) -> list[Entitlement] | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.id == account_id)
            account = session.exec(account_query).one_or_none()

            if not account:
                return ErrorCode.USER_NOT_FOUND

            filtered_entitlements = select(Entitlement).where(
                Entitlement.owner_id == account.id,
                Entitlement.grantDate <= datetime.now(),  # type: ignore
                or_(
                    Entitlement.terminationDate == None,
                    Entitlement.terminationDate >= datetime.now(),  # type: ignore
                ),
            )

            if groupName:
                filtered_entitlements = filtered_entitlements.where(
                    Entitlement.groupName == groupName
                )

            if entitlementTag:
                filtered_entitlements = filtered_entitlements.where(
                    Entitlement.tag == entitlementTag
                )

            return list(session.exec(filtered_entitlements).all())

    def account_entitle(
        self, account_id: int, serial_key_str: str
    ) -> list[Entitlement] | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.id == account_id)
            account = session.exec(account_query).one_or_none()

            if not account:
                return ErrorCode.USER_NOT_FOUND

            serial_key_query = select(SerialKey).where(SerialKey.key == serial_key_str)
            serial_key = session.exec(serial_key_query).one_or_none()

            if not serial_key:
                return ErrorCode.CODE_NOT_FOUND

            if serial_key.used:
                return ErrorCode.CODE_ALREADY_USED

            if not serial_key.reusable:
                serial_key.used = True

            entitlements = []

            for target in serial_key.targets:
                entitlement = Entitlement(
                    tag=target.tag,
                    owner=account,
                    groupName=target.groupName,
                    productId=target.productId,
                    version=target.version,
                )

                session.add(entitlement)
                session.commit()

                entitlements.append(entitlement)

            return entitlements

    def account_grant_entitlement(
        self, request: NuGrantEntitlementRequest
    ) -> bool | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.id == request.masterId)
            account = session.exec(account_query).one_or_none()

            if not account:
                return ErrorCode.USER_NOT_FOUND

            entitlement = Entitlement(
                tag=request.entitlementTag,
                owner=account,
                groupName=request.groupName,
                productId=request.productId,
                grantDate=request.grantStartDate,
                terminationDate=request.grantEndDate,
            )

            session.add(entitlement)
            session.commit()

            return True

    def persona_get_all(self, account_id: int) -> list[Persona] | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.id == account_id)
            account = session.exec(account_query).one_or_none()

            if not account:
                return ErrorCode.USER_NOT_FOUND

            return account.personas

    def persona_get(self, account_id: int, persona_name: str) -> Persona | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.id == account_id)
            account = session.exec(account_query).one_or_none()

            if not account:
                return ErrorCode.USER_NOT_FOUND

            for persona in account.personas:
                if persona.name == persona_name:
                    return persona

            return ErrorCode.USER_NOT_FOUND

    def persona_get_by_id(self, persona_id: int) -> Persona | ErrorCode:
        with Session(self._engine) as session:
            persona_query = select(Persona).where(Persona.id == persona_id)
            persona = session.exec(persona_query).one_or_none()

            if not persona:
                return ErrorCode.USER_NOT_FOUND

            return persona

    def persona_get_by_name(self, persona_name: str) -> Persona | ErrorCode:
        with Session(self._engine) as session:
            persona_query = select(Persona).where(Persona.name == persona_name)
            persona = session.exec(persona_query).one_or_none()

            if not persona:
                return ErrorCode.USER_NOT_FOUND

            return persona

    def persona_get_owner_id(self, persona_id: int) -> int | ErrorCode:
        with Session(self._engine) as session:
            persona_query = select(Persona).where(Persona.id == persona_id)
            persona = session.exec(persona_query).one_or_none()

            if not persona:
                return ErrorCode.USER_NOT_FOUND

            return persona.owner.id

    def persona_add(self, account_id: int, persona: Persona) -> bool | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.id == account_id)
            account = session.exec(account_query).one_or_none()

            if not account:
                return ErrorCode.USER_NOT_FOUND

            persona = Persona(owner=account, name=persona.name)

            session.add(persona)
            session.commit()

            return True

    def persona_delete(self, account_id: int, persona_id: int) -> bool | ErrorCode:
        with Session(self._engine) as session:
            account_query = select(Account).where(Account.id == account_id)
            account = session.exec(account_query).one_or_none()

            persona_query = select(Persona).where(Persona.id == persona_id)
            persona = session.exec(persona_query).one_or_none()

            if not account or not persona:
                return ErrorCode.USER_NOT_FOUND

            session.delete(persona)
            session.commit()

            return True

    def persona_search(self, search: str) -> list[Persona]:
        with Session(self._engine) as session:
            search = search.replace("*", "%").replace("_", "")
            personas_query = select(Persona).filter(Persona.name.ilike(search))  # type: ignore
            personas = session.exec(personas_query).all()

            return list(personas)

    def association_get(self, persona_id, target_id, association_type: AssocationType):
        with Session(self._engine) as session:
            association_query = select(Association).where(
                Association.owner_id == persona_id,
                Association.target_id == target_id,
                Association.type == association_type,
            )
            association = session.exec(association_query).one_or_none()

            return association

    def association_get_all(
        self, persona_id: int, assocation_type: AssocationType
    ) -> list[Association] | ErrorCode:
        with Session(self._engine) as session:
            persona_query = select(Persona).where(Persona.id == persona_id)
            persona = session.exec(persona_query).one_or_none()

            if not persona:
                return ErrorCode.USER_NOT_FOUND

            assocations_list = []

            for association in persona.associations:
                if association.type == assocation_type:
                    assocations_list.append(association)
                    # Preload the target persona
                    association.target

            return assocations_list

    def association_delete(
        self, association_id: int, association_target_id: int | None = None
    ) -> bool | ErrorCode:
        with Session(self._engine) as session:
            association_query = select(Association).where(
                Association.id == association_id
            )

            association_target = None

            if association_target_id:
                association_target_query = select(Association).where(
                    Association.id == association_target_id
                )

                association_target = session.exec(
                    association_target_query
                ).one_or_none()

            association = session.exec(association_query).one_or_none()

            if not association or (association_target_id and not association_target):
                return ErrorCode.SYSTEM_ERROR

            session.delete(association)
            if association_target:
                session.delete(association_target)
            session.commit()

            return True

    def association_add(
        self, owner_id: int, target_id: int, type: AssocationType
    ) -> Association | ErrorCode:
        with Session(self._engine) as session:
            association_query = select(Association).where(
                Association.owner_id == owner_id,
                Association.target_id == target_id,
                Association.type == type,
            )
            existing_association = session.exec(association_query).one_or_none()

            if existing_association:
                return ErrorCode.SYSTEM_ERROR

            association = Association(
                owner_id=owner_id,
                target_id=target_id,
                type=type,
            )

            session.add(association)
            session.commit()
            session.refresh(association)

            return association

    def ranking_get(self, persona_id: int, keys: list[str]) -> list[Ranking]:
        with Session(self._engine) as session:
            stats_query = select(Ranking).where(Ranking.owner_id == persona_id)
            stats_query = stats_query.where(or_(*[Ranking.key == key for key in keys]))

            stats = session.exec(stats_query).all()
            return list(stats)

    def ranking_get_ranked(
        self, persona_id: int, keys: list[str]
    ) -> list[tuple[Ranking, int]]:
        with Session(self._engine) as session:
            stats_query = select(
                Ranking,
                func.rank().over(
                    partition_by=Ranking.key, order_by=Ranking.value.desc()  # type: ignore
                ),
            ).where(Ranking.owner_id == persona_id)

            stats_query = stats_query.where(or_(*[Ranking.key == key for key in keys]))
            stats = session.exec(stats_query).all()
            return list(stats)

    def ranking_get_ranked_owners(
        self, persona_ids: list[int], keys: list[str]
    ) -> list[tuple[Ranking, int]]:
        with Session(self._engine) as session:
            stats_query = select(
                Ranking,
                func.rank().over(
                    partition_by=Ranking.key, order_by=Ranking.value.desc()  # type: ignore
                ),
            ).where(
                or_(*[Ranking.owner_id == persona_id for persona_id in persona_ids])
            )

            stats_query = stats_query.where(or_(*[Ranking.key == key for key in keys]))
            stats = session.exec(stats_query).all()
            return list(stats)

    def ranking_leaderboard_get(
        self, queryKey: str, minRank: int, maxRank: int
    ) -> list[tuple[Ranking, int]]:
        with Session(self._engine) as session:
            stats_query = select(
                Ranking,
                func.rank()
                .over(
                    partition_by=Ranking.key, order_by=Ranking.value.desc()  # type: ignore
                )
                .between(minRank, maxRank),
            ).where(
                Ranking.key == queryKey,
            )

            stats = session.exec(stats_query).all()
            return list(stats)

    def ranking_set(
        self, persona_id: int, key: str, value: Decimal, update_type: StatUpdateType
    ) -> bool:
        with Session(self._engine) as session:
            stat_query = select(Ranking).where(
                Ranking.owner_id == persona_id, Ranking.key == key
            )
            stat = session.exec(stat_query).one_or_none()

            if not stat:
                stat = Ranking(owner_id=persona_id, key=key, value=value)
            else:
                if update_type == StatUpdateType.RelativeValue:
                    stat.value += value
                else:
                    stat.value = value

            session.add(stat)
            session.commit()

            return True

    def record_get(self, persona_id: int, type: RecordName) -> list[Record]:
        with Session(self._engine) as session:
            record_query = select(Record).where(Record.owner_id == persona_id)
            record_query = record_query.where(Record.type == type)

            records = session.exec(record_query).all()

            return list(records)

    def record_add(
        self, persona_id: int, type: RecordName, key: int, value: str
    ) -> bool:
        with Session(self._engine) as session:
            record = Record(owner_id=persona_id, type=type, key=key, value=value)
            session.add(record)
            session.commit()

            return True

    def record_update(
        self, persona_id: int, type: RecordName, key: int, value: str
    ) -> bool:
        with Session(self._engine) as session:
            record_query = select(Record).where(
                Record.owner_id == persona_id, Record.type == type, Record.key == key
            )
            record = session.exec(record_query).one_or_none()

            if not record:
                return False

            record.value = value

            session.add(record)
            session.commit()

            return True

    def message_get(self, message_id: int) -> Message | None:
        with Session(self._engine) as session:
            message_query = select(Message).where(Message.id == message_id)
            message = session.exec(message_query).one_or_none()

            return message

    def message_get_all(self, persona_id: int) -> list[Message]:
        with Session(self._engine) as session:
            message_query = select(Message).where(Message.recipient_id == persona_id)
            messages = session.exec(message_query).all()

            return list(messages)

    def message_add(self, messageData: Message) -> Message:
        with Session(self._engine) as session:
            attachments = []

            for attachment in messageData.attachments:
                attachment = MessageAttachment(
                    key=attachment.key, type=attachment.type, data=attachment.data
                )

                session.add(attachment)
                session.commit()

                attachments.append(attachment)

            message = Message(
                sender_id=messageData.sender_id,
                recipient_id=messageData.recipient.id,
                messageType=messageData.messageType,
                deliveryType=messageData.deliveryType,
                purgeStrategy=messageData.purgeStrategy,
                expiration=messageData.expiration,
                attachments=attachments,
            )

            session.add(message)
            session.commit()
            session.refresh(message)

            return message

    def message_delete(self, message_id: int) -> bool:
        with Session(self._engine) as session:
            message_query = select(Message).where(Message.id == message_id)
            message = session.exec(message_query).one_or_none()

            if not message:
                return False

            session.delete(message)
            session.commit()

            return True

    def lobby_get(self, lobby_id: int) -> Lobby | None:
        with Session(self._engine) as session:
            lobby_query = select(Lobby).where(Lobby.id == lobby_id)
            lobby = session.exec(lobby_query).one_or_none()

            return lobby

    def lobby_get_all(self) -> list[Lobby]:
        with Session(self._engine) as session:
            lobby_query = select(Lobby)
            lobbies = session.exec(lobby_query).all()

            return list(lobbies)

    def lobby_get_games(self, request: GetGameListRequest) -> list[Game]:
        with Session(self._engine) as session:
            games_query = select(Game).where(Game.lobbyId == request.LID)

            if not request.GID:
                request.GID = 0

            games_query = games_query.where(
                Game.id >= request.GID,
                Game.gameType == request.TYPE,
                Game.joinMode == JoinMode.OPEN,
            )

            # Filter games
            if request.FILTER_FAV_ONLY:
                games_query = games_query.where(Game.serverName == request.FAV_GAME)

            if request.FILTER_NOT_FULL:
                games_query = games_query.where(Game.maxPlayers > Game.activePlayers)

            if request.FILTER_MIN_SIZE:
                games_query = games_query.where(
                    Game.activePlayers >= request.FILTER_MIN_SIZE
                )

            if request.FILTER_ATTR_U_gameMod:
                games_query = games_query.where(
                    Game.gameMod == request.FILTER_ATTR_U_gameMod
                )

            if request.FILTER_NOT_PRIVATE:
                games_query = games_query.where(Game.gamePublic == True)

            if request.FILTER_NOT_CLOSED:
                games_query = games_query.where(Game.joinMode != JoinMode.CLOSED)

            games = session.exec(games_query).all()[: request.COUNT]
            return list(games)

    def lobby_get_games_count(self, lobby_id: int) -> int:
        with Session(self._engine) as session:
            lobby_query = select(Lobby).where(Lobby.id == lobby_id)
            lobby = session.exec(lobby_query).one_or_none()

            if not lobby:
                return 0

            return len(lobby.games)

    def game_create(
        self,
        persona_id: int,
        data: CreateGameRequest,
        clientPlatform: ClientPlatform,
        clientLocale: ClientLocale,
        clientVersion: str,
    ) -> Game | ErrorCode:
        with Session(self._engine) as session:
            persona_query = select(Persona).where(Persona.id == persona_id)
            persona = session.exec(persona_query).one_or_none()

            if not persona or not persona.owner.serviceAccount:
                return ErrorCode.USER_NOT_FOUND

            # Try to find the game with specified UGID
            game_query = select(Game).where(Game.ugid == data.UGID)
            game = session.exec(game_query).one_or_none()

            if game:
                if (
                    game.secret == data.SECRET.get_secret_value()
                    and game.joinMode != JoinMode.OPEN
                ):
                    # Refresh the encryption key, and apply new values
                    game.ekey = secrets.token_urlsafe(16)

                    game.serverName = data.NAME
                    game.addrIp = str(data.INT_IP)
                    game.addrPort = data.INT_PORT
                    game.platform = clientPlatform
                    game.gameType = data.TYPE
                    game.queueLength = data.QLEN
                    game.maxPlayers = data.MAX_PLAYERS
                    game.numObservers = data.B_numObservers
                    game.maxObservers = data.B_maxObservers
                    game.serverHardcore = data.B_U_Hardcore
                    game.serverHasPassword = data.B_U_HasPassword
                    game.serverPunkbuster = data.B_U_Punkbuster
                    game.clientVersion = clientVersion
                    game.serverVersion = data.B_version
                    game.joinMode = data.JOIN

                    session.add(game)
                    session.commit()
                    session.refresh(game)

                    return game

            # Create a new game

            # If there's no room in a lobby, or there's no lobby, create a new one
            lobby_query = select(Lobby, func.count())
            lobby_return = session.exec(lobby_query).one_or_none()

            if not lobby_return:
                count = 1

                lobby = Lobby(
                    name=f"bfbc2{clientPlatform.value}{count}", locale=clientLocale
                )
                session.add(lobby)
            else:
                lobby, count = lobby_return

                if not lobby or len(lobby.games) >= lobby.maxGames:
                    count = count + 1

                    lobby = Lobby(
                        name=f"bfbc2{clientPlatform.value}{'{:02d}'.format(count)}",
                        locale=clientLocale,
                    )
                    session.add(lobby)

            game = Game(
                lobby=lobby,
                owner=persona,
                serverName=data.NAME,
                addrIp=str(data.INT_IP),
                addrPort=data.INT_PORT,
                platform=clientPlatform,
                gameType=data.TYPE,
                queueLength=data.QLEN,
                maxPlayers=data.MAX_PLAYERS,
                numObservers=data.B_numObservers,
                maxObservers=data.B_maxObservers,
                serverHardcore=data.B_U_Hardcore,
                serverHasPassword=data.B_U_HasPassword,
                serverPunkbuster=data.B_U_Punkbuster,
                clientVersion=clientVersion,
                serverVersion=data.B_version,
                joinMode=data.JOIN,
                ugid=secrets.token_urlsafe(16),
                ekey=secrets.token_urlsafe(16),
                secret=secrets.token_urlsafe(64),
            )

            session.add(game)
            session.commit()
            session.refresh(game)

            return game

    def game_update(
        self, request: UpdateGameRequest | UpdateGameDetailsRequest
    ) -> bool:
        with Session(self._engine) as session:
            game_query = select(Game).where(Game.id == request.GID)
            game = session.exec(game_query).one_or_none()

            if not game:
                return False

            data_to_update = request.model_dump(exclude_none=True)

            for key, value in data_to_update.items():
                if hasattr(game, key):
                    setattr(game, key, value)

            session.add(game)
            session.commit()

            return True

    def game_disable(self, game_id: int) -> bool:
        with Session(self._engine) as session:
            game_query = select(Game).where(Game.id == game_id)
            game = session.exec(game_query).one_or_none()

            if not game:
                return False

            game.joinMode = JoinMode.CLOSED

            session.add(game)
            session.commit()

            return True

    def game_get(self, lobby_id: int, game_id: int) -> Game | None:
        with Session(self._engine) as session:
            game_query = select(Game).where(
                Game.lobbyId == lobby_id, Game.id == game_id
            )
            game = session.exec(game_query).one_or_none()

            return game

    def game_find(self, gameType: GameType, level: int) -> Game | None:
        with Session(self._engine) as session:
            game_query = select(Game).where(
                Game.gameType == gameType, Game.gameLevel == level
            )
            game = session.exec(game_query).one_or_none()

            return game
