import os
from abc import ABC, abstractmethod


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
            self.register(nuid=account[0], password=account[1], serviceAccount=True)

    @abstractmethod
    def register(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def login(self, **kwargs):
        raise NotImplementedError()
