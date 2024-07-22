from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.PingSite import PingSite


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
