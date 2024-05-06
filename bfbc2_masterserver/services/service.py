from abc import ABC, abstractmethod


class Service(ABC):
    def __init__(self, plasma) -> None:
        self.resolvers = {}
        self.generators = {}
        self.plasma = plasma

    @abstractmethod
    def _get_resolver(self, txn):
        raise NotImplementedError("Service must implement __get_resolver")

    @abstractmethod
    def _get_generator(self, txn):
        raise NotImplementedError("Service must implement __get_creator")

    def handle(self, data):
        txn = data["TXN"]

        resolver = self._get_resolver(txn)
        return resolver(data)

    def start_transaction(self, txn, data):
        """Start a scheduled transaction"""

        creator = self._get_generator(txn)
        return creator(data)
