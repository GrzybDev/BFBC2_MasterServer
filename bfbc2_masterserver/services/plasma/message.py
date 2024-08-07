from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.message.GetMessages import (
    GetMessagesRequest,
    GetMessagesResponse,
)
from bfbc2_masterserver.messages.plasma.message.ModifySettings import (
    ModifySettingsRequest,
    ModifySettingsResponse,
)
from bfbc2_masterserver.models.plasma.database.Message import Message
from bfbc2_masterserver.models.plasma.Message import Attachment, MessageResponse, Target


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

    def __handle_get_messages(
        self, data: GetMessagesRequest
    ) -> GetMessagesResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        messages_db: list[Message] = self.database.message_get(
            self.connection.persona.id
        )

        messages: list[MessageResponse] = [
            MessageResponse(
                attachments=[
                    Attachment(
                        key=attachment.key, type=attachment.type, data=attachment.data
                    )
                    for attachment in message.attachments
                ],
                deliveryType=message.deliveryType,
                messageId=message.id,
                messageType=message.messageType,
                purgeStrategy=message.purgeStrategy,
                from_=Target(
                    name=message.sender.name,
                    id=message.sender.id,
                    type=1,
                ),
                to=[
                    Target(
                        name=message.recipient.name,
                        id=message.recipient.id,
                        type=1,
                    )
                ],
                timeSent=message.timeSent,
                expiration=message.expiration,
            )
            for message in messages_db
        ]

        return GetMessagesResponse(messages=messages)
