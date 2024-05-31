from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.messages.plasma.message.ModifySettings import (
    ModifySettingsRequest,
    ModifySettingsResponse,
)
from bfbc2_masterserver.services.service import Service


class ExtensibleMessageService(Service):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[Transaction.ModifySettings] = (
            self.__handle_modify_settings,
            ModifySettingsRequest,
        )

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

    def __handle_modify_settings(self, data: ModifySettingsRequest):
        return ModifySettingsResponse()
