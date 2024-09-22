import logging
from abc import ABC, abstractmethod

from pydantic import ValidationError

from bfbc2_masterserver.dataclasses.Connection import BaseConnection
from bfbc2_masterserver.dataclasses.Handler import BasePlasmaHandler
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError, TransactionSkip
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction

logger = logging.getLogger(__name__)


class PlasmaService(ABC):

    def __init__(self, plasma: BasePlasmaHandler) -> None:
        """
        The constructor for the Service class.

        Initializes the resolvers and generators dictionaries and sets the Plasma object.

        Parameters:
            plasma: The Plasma object associated with this service.
        """

        self.resolvers = {}
        self.generators = {}

        self.connection = plasma.client.connection
        self.database = plasma.manager.database
        self.manager = plasma.manager
        self.redis = plasma.manager.redis
        self.plasma = plasma

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
