from abc import ABC, abstractmethod


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

    def handle(self, data):
        """
        Handles incoming data by getting the appropriate resolver and calling it.

        Parameters:
            data (dict): The incoming data.

        Returns:
            The result of the resolver function.
        """

        resolver = self._get_resolver(data["TXN"])
        return resolver(data)

    def start_transaction(self, txn, data):
        """
        Starts a scheduled transaction by getting the appropriate generator and calling it.

        Parameters:
            txn (str): The name of the transaction.
            data (dict): The data for the transaction.

        Returns:
            The result of the generator function.
        """

        creator = self._get_generator(txn)
        return creator(data)
