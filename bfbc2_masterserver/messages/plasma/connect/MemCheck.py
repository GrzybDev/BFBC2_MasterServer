from bfbc2_masterserver.messages.plasma.MemCheck import MemCheck
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class MemCheckRequest(PlasmaTransaction):
    """
    This class represents a MemCheck request message.

    Attributes:
        memcheck (MemCheck): The MemCheck object.
        type (int): The type of the MemCheck.
        salt (str): The salt value for the MemCheck.

    """

    memcheck: MemCheck
    type: int
    salt: str


class MemCheckResult(PlasmaTransaction):
    """
    This class represents a MemCheck result message.

    Attributes:
        result (str): The result of the MemCheck.
    """

    result: str
