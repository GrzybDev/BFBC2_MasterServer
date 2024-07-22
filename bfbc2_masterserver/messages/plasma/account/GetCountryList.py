from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Country import Country


class GetCountryListRequest(PlasmaTransaction):
    """
    This class represents a GetCountryList request message.
    """


class GetCountryListResponse(PlasmaTransaction):
    """
    This class represents a GetCountryList response message.

    Attributes:
        countryList (list[Country]): The country list.
    """

    countryList: list[Country]
