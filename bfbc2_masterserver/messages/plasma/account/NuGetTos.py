from typing import Optional

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuGetTosRequest(PlasmaTransaction):
    """
    This class represents a NuGetTos request message.

    Attributes:
        countryCode (str): The country code.
    """

    countryCode: Optional[str] = None


class NuGetTosResponse(PlasmaTransaction):
    """
    This class represents a NuGetTos response message.

    Attributes:
        tos (str): The terms of service content.
        version (str): The terms of service version.
    """

    tos: str
    version: str
