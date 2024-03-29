from abc import ABC, abstractmethod

from Plasma.error import TransactionError


class Service(ABC):
    def __init__(self, connection) -> None:
        self.resolver_map = {}
        self.creator_map = {}
        self.connection = connection

    @abstractmethod
    def _get_resolver(self, txn):
        raise NotImplementedError("Service must implement __get_resolver")

    @abstractmethod
    def _get_creator(self, txn):
        raise NotImplementedError("Service must implement __get_creator")

    async def handle(self, data):
        txn = data.Get("TXN")

        try:
            resolver = self._get_resolver(txn)
        except KeyError:
            self.connection.logger.error(
                f"Invalid transaction {txn} for service {self}"
            )
            return TransactionError(TransactionError.Code.SYSTEM_ERROR)

        try:
            return await resolver(data)
        except Exception:
            self.connection.logger.exception(f"Failed to handle transaction {txn}")
            return TransactionError(TransactionError.Code.SYSTEM_ERROR)

    async def start_transaction(self, txn, data):
        """Start a scheduled transaction"""

        try:
            creator = self._get_creator(txn)
        except KeyError:
            self.connection.logger.error(
                f"Invalid transaction {txn} for service {self}"
            )
            return TransactionError(TransactionError.Code.SYSTEM_ERROR)

        try:
            return await creator(data)
        except Exception:
            self.connection.logger.exception(
                f"Failed to create unscheduled transaction {txn}"
            )
            return TransactionError(TransactionError.Code.SYSTEM_ERROR)
