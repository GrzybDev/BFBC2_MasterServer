from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.messages.plasma.account.GetCountryList import (
    GetCountryListRequest,
    GetCountryListResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuGetTos import (
    NuGetTosRequest,
    NuGetTosResponse,
)
from bfbc2_masterserver.services.service import Service
from bfbc2_masterserver.tools.country_list import getLocalizedCountryList
from bfbc2_masterserver.tools.terms_of_service import getLocalizedTOS


class AccountService(Service):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[Transaction.GetCountryList] = (
            self.__handle_get_country_list,
            GetCountryListRequest,
        )
        self.resolvers[Transaction.NuGetTos] = self.__handle_nu_get_tos, NuGetTosRequest

    def _get_resolver(self, txn):
        """
        Gets the resolver for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The resolver function for the transaction.
        """
        return self.resolvers[Transaction(txn)]

    def _get_generator(self, txn):
        """
        Gets the generator for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The generator function for the transaction.
        """
        return self.generators[Transaction(txn)]

    def __handle_get_country_list(self, data: GetCountryListRequest):
        """
        Handles the GetCountryList transaction.

        Parameters:
            data (dict): The incoming data.

        Returns:
            The response to the transaction.
        """

        response = GetCountryListResponse(
            countryList=getLocalizedCountryList(self.plasma.clientLocale)
        )

        return Message(data=response.model_dump(exclude_none=True))

    def __handle_nu_get_tos(self, data: NuGetTosRequest):
        """
        Handles the NuGetTos transaction.

        Parameters:
            data (dict): The incoming data.

        Returns:
            The response to the transaction.
        """

        # In theory everything shows that here we should send the TOS for the selected country code.
        # However, this doesn't seem to be the case. Original server sends the same TOS for every country code, only (game) language seems to have any effect.

        tos = getLocalizedTOS(self.plasma.clientLocale)

        response = NuGetTosResponse(tos=tos["tos"], version=tos["version"])
        return Message(data=response.model_dump(exclude_none=True))
