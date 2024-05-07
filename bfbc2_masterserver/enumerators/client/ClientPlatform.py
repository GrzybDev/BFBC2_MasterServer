from enum import Enum


class ClientPlatform(Enum):
    """
    The ClientPlatform class is a subclass of the Enum class from the enum module.

    This class represents various client platforms that can be used in the system. Each platform is represented by a unique string value.

    Attributes:
        PC (str): The string value for PC platform.
        PS3 (str): The string value for PlayStation 3 platform.
        XBOX360 (str): The string value for Xbox 360 platform.
    """

    PC = "PC"
    PS3 = "ps3"
    XBOX360 = "xenon"
