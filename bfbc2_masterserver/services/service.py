import logging
from abc import ABC, abstractmethod

from pydantic import SecretStr, ValidationError
from redis import Redis

from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.error import TransactionError, TransactionSkip
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction

logger = logging.getLogger(__name__)


class Service(ABC):
    """
    The Service class is an abstract base class that represents a service in a communication system.

    Attributes:
        resolvers (dict): A dictionary mapping transaction names to resolver functions.
        generators (dict): A dictionary mapping transaction names to generator functions.
        plasma: The Plasma object associated with this service.

    Methods:
        __init__(self, plasma): The constructor for the Service class.
        _get_resolver(self, txn): An abstract method that gets the resolver for a given transaction.
        _get_generator(self, txn): An abstract method that gets the generator for a given transaction.
        handle(self, data): Handles incoming data by getting the appropriate resolver and calling it.
        start_transaction(self, txn, data): Starts a scheduled transaction by getting the appropriate generator and calling it.
    """

    __ignore_validation_errors: list[str] = [Transaction.NuAddAccount.value]

    def __init__(self, plasma) -> None:
        """
        The constructor for the Service class.

        Initializes the resolvers and generators dictionaries and sets the Plasma object.

        Parameters:
            plasma: The Plasma object associated with this service.
        """

        self.resolvers = {}
        self.generators = {}
        self.plasma = plasma
        self.database: BaseDatabase = plasma.manager.database
        self.redis: Redis = plasma.manager.redis

    @abstractmethod
    def _get_resolver(self, txn):
        """
        An abstract method that gets the resolver for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError("Service must implement __get_resolver")

    @abstractmethod
    def _get_generator(self, txn):
        """
        An abstract method that gets the generator for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError("Service must implement __get_creator")

    def handle(self, message):
        """
        Handles incoming data by getting the appropriate resolver and calling it.

        Parameters:
            data (dict): The incoming data.

        Returns:
            The result of the resolver function.
        """

        txn = message.data["TXN"]
        resolver, model = self._get_resolver(txn)

        try:
            message.data = model.model_validate(message.data)

            # Log the incoming message
            logger.debug(
                f"{self.plasma.ws.client.host}:{self.plasma.ws.client.port} -> {message}"
            )
        except ValidationError as e:
            logger.exception(
                f"{self.plasma.ws.client.host}:{self.plasma.ws.client.port} -> {e}",
                exc_info=True,
            )

            if txn not in self.__ignore_validation_errors:
                return TransactionError(ErrorCode.PARAMETERS_ERROR)
            else:
                message.data = e

        response_data = resolver(message.data)

        if isinstance(response_data, TransactionSkip):
            return response_data
        elif isinstance(message.data, ValidationError):
            message.data = PlasmaTransaction(TXN=txn)

        response = self.plasma.finish_message(message, response_data)

        # Log the outgoing message
        logger.debug(
            f"{self.plasma.ws.client.host}:{self.plasma.ws.client.port} <- {response}"
        )

        return response

    def create_message(self, message, data):
        """
        Starts a scheduled transaction by getting the appropriate generator and calling it.

        Parameters:
            txn (str): The name of the transaction.
            data (dict): The data for the transaction.

        Returns:
            The result of the generator function.
        """

        creator = self._get_generator(message.data.TXN)
        request = creator(data)

        message = self.plasma.finish_message(message, request, noTransactionID=True)

        # Log the outgoing message
        logger.debug(
            f"{self.plasma.ws.client.host}:{self.plasma.ws.client.port} <- {message}"
        )

        return message
