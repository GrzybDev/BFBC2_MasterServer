from enum import Enum


class MessageFrom(Enum):
    """
    The MessageFrom class is a subclass of the Enum class from the enum module.

    This class represents the source of a message in the system. Each source is represented by a unique integer value.

    Attributes:
        Plasma (int): The integer value for a message from Plasma.
        Theater (int): The integer value for a message from Theater.
    """

    Plasma = 0
    Theater = 1
