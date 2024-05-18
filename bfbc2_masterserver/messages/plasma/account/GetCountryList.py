from bfbc2_masterserver.messages.plasma.Country import Country
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


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
