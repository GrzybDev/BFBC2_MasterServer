import logging
from abc import ABC, abstractmethod

from pydantic import ValidationError
from redis import Redis

from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.dataclasses.Handler import BaseHandler
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError, TransactionSkip
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction

logger = logging.getLogger(__name__)


class PlasmaService(ABC):

    __ignore_validation_errors: list[str] = [FESLTransaction.NuAddAccount.value]

    def __init__(self, plasma: BaseHandler) -> None:
        """
        The constructor for the Service class.

        Initializes the resolvers and generators dictionaries and sets the Plasma object.

        Parameters:
            plasma: The Plasma object associated with this service.
        """

        self.resolvers = {}
        self.generators = {}

        self.plasma: BaseHandler = plasma
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

    def handle(self, message: Message) -> TransactionError | TransactionSkip | Message:
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
            logger.debug(f"{self.plasma.get_client_address()} -> {message}")
        except ValidationError as e:
            logger.exception(
                f"{self.plasma.get_client_address()} -> {e}",
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

        response: Message = self.plasma.finish_message(message, response_data)

        # Log the outgoing message
        logger.debug(f"{self.plasma.get_client_address()} <- {response}")
        return response

    def create_message(self, message: Message, data: PlasmaTransaction) -> Message:
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

        finished_message: Message = self.plasma.finish_message(
            message, request, noTransactionID=True
        )

        # Log the outgoing message
        logger.debug(f"{self.plasma.get_client_address()} <- {finished_message}")
        return finished_message
