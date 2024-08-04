import os
from abc import ABC, abstractmethod
from typing import Tuple

from pydantic import SecretStr

from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.messages.plasma.ranking.GetTopNAndStats import Leaderboard
from bfbc2_masterserver.messages.theater.commands.CreateGame import CreateGameRequest
from bfbc2_masterserver.messages.theater.commands.GetGameList import GameData
from bfbc2_masterserver.messages.theater.commands.GetLobbyList import Lobby
from bfbc2_masterserver.messages.theater.commands.UpdateGame import UpdateGameRequest
from bfbc2_masterserver.messages.theater.commands.UpdateGameDetails import (
    UpdateGameDetailsRequest,
)
from bfbc2_masterserver.models.plasma.database.Account import Account
from bfbc2_masterserver.models.plasma.database.Association import Association
from bfbc2_masterserver.models.plasma.database.Entitlement import Entitlement
from bfbc2_masterserver.models.plasma.database.Game import GameServer
from bfbc2_masterserver.models.plasma.database.Message import Message
from bfbc2_masterserver.models.plasma.database.Persona import Persona
from bfbc2_masterserver.models.plasma.database.Record import Record
from bfbc2_masterserver.models.plasma.database.Stats import RankedStat, Stat


class BaseDatabase(ABC):

    def __init__(self, connection_string: str):
        self.secret_key = os.environ.get("SECRET_KEY", "bfbc2emu")
        self.algorithm = os.environ.get("ALGORITHM_OVERRIDE", "HS256")

    def prepare_db(self):
        service_accounts = [
            ("bfbc2.server.pc@ea.com", "Che6rEPA"),
            ("bfbc.server.ps3@ea.com", "zAmeH7bR"),
            ("bfbc.server.xenon@ea.com", "B8ApRavE"),
        ]

        default_keys = [
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
                        "group": "BFBC2PC",
                        "product": "OFB-EAST:40873",
                    },
                ],
            },
        ]

        for account in service_accounts:
            self.register(
                nuid=account[0], password=SecretStr(account[1]), serviceAccount=True
            )

        for key in default_keys:
            self._add_key(key, consumable=False)

        self._add_lobby("bfbc2PC01", "en_US")

    @abstractmethod
    def register(self, **kwargs) -> bool | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def login(self, **kwargs) -> Account | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def get_account(self, account_id) -> Account | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def get_personas(self, account_id) -> list[str]:
        raise NotImplementedError()

    @abstractmethod
    def add_persona(self, account_id, name) -> bool | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def disable_persona(self, account_id, name) -> bool | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def get_persona(self, account_id, name) -> Persona | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def get_persona_by_id(self, persona_id) -> Persona | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def accept_tos(self, account_id, version) -> bool | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def is_entitled(self, account_id, entitlement_id) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def entitle_game(self, account_id, key) -> bool | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def get_assocation(
        self, persona_id: int, association_type: AssocationType
    ) -> Tuple[str, list[Association]] | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def get_entitlements(
        self, account_id, groupName, entitlementTag
    ) -> list[Entitlement] | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def _add_key(self, data, consumable=True) -> None:
        raise NotImplementedError()

    @abstractmethod
    def entitle_user(self, account_id, key) -> list[Entitlement] | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def get_messages(self, persona_id) -> list[Message]:
        raise NotImplementedError()

    @abstractmethod
    def get_stats(self, persona_id, keys) -> list[Stat]:
        raise NotImplementedError()

    @abstractmethod
    def get_ranked_stats(self, persona_id, keys) -> list[RankedStat]:
        raise NotImplementedError()

    @abstractmethod
    def get_leaderboard(self, keys) -> list[Leaderboard]:
        raise NotImplementedError()

    @abstractmethod
    def get_records(self, persona_id, type) -> list[Record]:
        raise NotImplementedError()

    @abstractmethod
    def get_lobbies(self) -> list[Lobby]:
        raise NotImplementedError()

    @abstractmethod
    def _add_lobby(self, name, locale) -> bool | ErrorCode:
        raise NotImplementedError()

    @abstractmethod
    def get_lobby_games_count(self, lobby_id) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_lobby_games(self, lobby_id) -> list[GameData]:
        raise NotImplementedError()

    @abstractmethod
    def create_game(self, ownerId: int, request: CreateGameRequest) -> GameServer:
        raise NotImplementedError()

    @abstractmethod
    def update_game(
        self, request: UpdateGameRequest | UpdateGameDetailsRequest
    ) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def disable_game(self, gid: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def find_game(self, prefGamemode, prefLevel) -> GameServer | None:
        raise NotImplementedError()

    @abstractmethod
    def get_game(self, lid, gid) -> GameServer | None:
        raise NotImplementedError()
