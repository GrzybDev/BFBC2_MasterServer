import os
from abc import ABC, abstractmethod
from typing import Tuple

from pydantic import SecretStr

from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.messages.Account import Account
from bfbc2_masterserver.messages.Persona import Persona
from bfbc2_masterserver.messages.plasma.Association import Association
from bfbc2_masterserver.messages.plasma.Entitlement import Entitlement


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
