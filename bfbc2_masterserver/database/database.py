import os
from abc import ABC, abstractmethod

from pydantic import SecretStr

from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType


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

        for account in service_accounts:
            self.register(
                nuid=account[0], password=SecretStr(account[1]), serviceAccount=True
            )

    @abstractmethod
    def register(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def login(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get_personas(self, account_id) -> list[str]:
        raise NotImplementedError()

    @abstractmethod
    def add_persona(self, account_id, name):
        raise NotImplementedError()

    @abstractmethod
    def disable_persona(self, account_id, name):
        raise NotImplementedError()

    @abstractmethod
    def get_persona(self, account_id, name):
        raise NotImplementedError()

    @abstractmethod
    def accept_tos(self, account_id, version):
        raise NotImplementedError()

    @abstractmethod
    def is_entitled(self, account_id, entitlement_id):
        raise NotImplementedError()

    @abstractmethod
    def entitle_game(self, account, key):
        raise NotImplementedError()

    @abstractmethod
    def get_assocation(self, persona_id: int, association_type: AssocationType):
        raise NotImplementedError()

    @abstractmethod
    def get_entitlements(self, account_id):
        raise NotImplementedError()
