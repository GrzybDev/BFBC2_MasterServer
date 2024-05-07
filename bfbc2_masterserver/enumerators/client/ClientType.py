from enum import Enum


class ClientType(Enum):
    """
    The ClientType class is a subclass of the Enum class from the enum module.

    This class represents various types of clients that can be used in the system. Each client type is represented by a unique string value.

    Attributes:
        Client (str): The string value for a client.
        Server (str): The string value for a server.
    """

    Client = ""
    Server = "server"
