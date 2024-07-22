from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.MemCheck import MemCheck


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
