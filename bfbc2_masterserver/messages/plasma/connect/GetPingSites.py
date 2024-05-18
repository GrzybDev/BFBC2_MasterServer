from bfbc2_masterserver.messages.plasma.PingSite import PingSite
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GetPingSitesRequest(PlasmaTransaction):
    """
    This class represents a GetPingSites request message.
    """


class GetPingSitesResponse(PlasmaTransaction):
    """
    This class represents a GetPingSites response message.

    Attributes:
        pingSite (list[PingSite]): The ping sites.
        minPingSitesToPing (int): The minimum number of ping sites to ping.
    """

    pingSite: list[PingSite]
    minPingSitesToPing: int
