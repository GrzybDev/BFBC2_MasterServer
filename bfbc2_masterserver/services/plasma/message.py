from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.messages.plasma.message.GetMessages import (
    GetMessagesRequest,
    GetMessagesResponse,
)
from bfbc2_masterserver.messages.plasma.message.ModifySettings import (
    ModifySettingsRequest,
    ModifySettingsResponse,
)
from bfbc2_masterserver.models.plasma.database.Message import Message


class ExtensibleMessageService(PlasmaService):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[FESLTransaction.ModifySettings] = (
            self.__handle_modify_settings,
            ModifySettingsRequest,
        )

        self.resolvers[FESLTransaction.GetMessages] = (
            self.__handle_get_messages,
            GetMessagesRequest,
        )

    def _get_resolver(self, txn):
        """
        Gets the resolver for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The resolver function for the transaction.
        """
        return self.resolvers[FESLTransaction(txn)]

    def _get_generator(self, txn):
        """
        Gets the generator for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The generator function for the transaction.
        """
        return self.generators[FESLTransaction(txn)]

    def __handle_modify_settings(
        self, data: ModifySettingsRequest
    ) -> ModifySettingsResponse:
        return ModifySettingsResponse()

    def __handle_get_messages(self, data: GetMessagesRequest) -> GetMessagesResponse:
        messages: list[Message] = self.database.get_messages(
            self.plasma.connection.personaId
        )
        return GetMessagesResponse(messages=messages)
