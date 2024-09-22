from datetime import datetime, timedelta

from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLService import FESLService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.message.AsyncMessageEvent import (
    AsyncMessageEvent,
)
from bfbc2_masterserver.messages.plasma.message.AsyncPurgedEvent import AsyncPurgedEvent
from bfbc2_masterserver.messages.plasma.message.DeleteMessages import (
    DeleteMessagesRequest,
    DeleteMessagesResponse,
)
from bfbc2_masterserver.messages.plasma.message.GetMessageAttachments import (
    GetMessageAttachmentsRequest,
    GetMessageAttachmentsResponse,
)
from bfbc2_masterserver.messages.plasma.message.GetMessages import (
    GetMessagesRequest,
    GetMessagesResponse,
)
from bfbc2_masterserver.messages.plasma.message.ModifySettings import (
    ModifySettingsRequest,
    ModifySettingsResponse,
)
from bfbc2_masterserver.messages.plasma.message.PurgeMessages import (
    PurgeMessagesRequest,
    PurgeMessagesResponse,
)
from bfbc2_masterserver.messages.plasma.message.SendMessage import (
    SendMessageRequest,
    SendMessageResponse,
)
from bfbc2_masterserver.models.plasma.database.Message import Message
from bfbc2_masterserver.models.plasma.database.MessageAttachment import (
    MessageAttachment,
)
from bfbc2_masterserver.models.plasma.Message import Attachment, MessageResponse, Target
from bfbc2_masterserver.models.plasma.Status import Status


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

        self.resolvers[FESLTransaction.SendMessage] = (
            self.__handle_send_message,
            SendMessageRequest,
        )

        self.resolvers[FESLTransaction.GetMessageAttachments] = (
            self.__handle_get_message_attachments,
            GetMessageAttachmentsRequest,
        )

        self.resolvers[FESLTransaction.DeleteMessages] = (
            self.__handle_delete_messages,
            DeleteMessagesRequest,
        )

        self.resolvers[FESLTransaction.PurgeMessages] = (
            self.__handle_purge_messages,
            PurgeMessagesRequest,
        )

        self.generators[FESLTransaction.AsyncMessageEvent] = (
            self.__create_async_message_event
        )
        self.generators[FESLTransaction.AsyncPurgedEvent] = (
            self.__create_async_purged_event
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

        messages_db: list[Message] = self.database.message_get_all(
            self.connection.persona.id
        )

        messages: list[MessageResponse] = [
            MessageResponse.model_validate(
                {
                    "attachments": [
                        Attachment(
                            key=attachment.key,
                            type=attachment.type,
                            data=attachment.data,
                        )
                        for attachment in message.attachments
                    ],
                    "deliveryType": message.deliveryType,
                    "messageId": message.id,
                    "messageType": message.messageType,
                    "purgeStrategy": message.purgeStrategy,
                    "from": Target(
                        name=message.sender.name,
                        id=message.sender.id,
                        type=1,
                    ),
                    "to": [
                        Target(
                            name=message.recipient.name,
                            id=message.recipient.id,
                            type=1,
                        )
                    ],
                    "timeSent": message.timeSent,
                    "expiration": message.expiration,
                }
            )
            for message in messages_db
        ]

        return GetMessagesResponse(messages=messages)

    def __handle_send_message(
        self, data: SendMessageRequest
    ) -> SendMessageResponse | TransactionError:
        if not self.connection.persona:
            return TransactionError(ErrorCode.SESSION_NOT_AUTHORIZED)

        expiration_date = datetime.now() + timedelta(seconds=data.expires)

        # While the game code only allows one recipient, the message schema allows for multiple recipients
        targetPersona = self.database.persona_get_by_id(data.to[0])

        if isinstance(targetPersona, ErrorCode):
            return TransactionError(targetPersona)

        message = Message(
            attachments=[
                MessageAttachment(
                    key=attachment.key,
                    type=attachment.type,
                    data=attachment.data,
                )
                for attachment in data.attachments
            ],
            deliveryType=data.deliveryType,
            messageType=data.messageType,
            purgeStrategy=data.purgeStrategy,
            sender_id=self.connection.persona.id,
            recipient=targetPersona,
            expiration=expiration_date,
        )

        result = self.database.message_add(message)

        accountId = self.database.persona_get_owner_id(targetPersona.id)

        if isinstance(accountId, ErrorCode):
            return TransactionError(accountId)

        receiverSession = self.plasma.manager.CLIENTS.get(accountId)

        if receiverSession:
            receiverSession.plasma.start_transaction(
                FESLService.MessageService,
                FESLTransaction.AsyncMessageEvent,
                AsyncMessageEvent.model_validate(
                    {
                        "attachments": [
                            Attachment(
                                key=attachment.key,
                                type=attachment.type,
                                data=attachment.data,
                            )
                            for attachment in message.attachments
                        ],
                        "deliveryType": message.deliveryType,
                        "messageId": result.id,
                        "messageType": message.messageType,
                        "purgeStrategy": message.purgeStrategy,
                        "from": Target(
                            name=self.connection.persona.name,
                            id=self.connection.persona.id,
                            type=1,
                        ),
                        "to": [
                            Target(
                                name=targetPersona.name,
                                id=targetPersona.id,
                                type=1,
                            )
                        ],
                        "timeSent": result.timeSent,
                        "expiration": message.expiration,
                    }
                ),
            ),

        return SendMessageResponse(
            messageId=result.id, status=[Status(userid=data.to[0], status=0)]
        )

    def __handle_get_message_attachments(
        self, data: GetMessageAttachmentsRequest
    ) -> GetMessageAttachmentsResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("GetMessageAttachments is not implemented.")

    def __handle_delete_messages(
        self, data: DeleteMessagesRequest
    ) -> DeleteMessagesResponse | TransactionError:
        for messageId in data.messageIds:
            message = self.database.message_get(messageId)
            self.database.message_delete(messageId)

            if message and (message.sender_id and message.recipient_id):
                senderSession = self.plasma.manager.CLIENTS.get(message.sender_id)
                receiverSession = self.plasma.manager.CLIENTS.get(message.recipient_id)

                if senderSession:
                    senderSession.plasma.start_transaction(
                        FESLService.MessageService,
                        FESLTransaction.AsyncPurgedEvent,
                        AsyncPurgedEvent(messageIds=[messageId]),
                    )

                if receiverSession:
                    receiverSession.plasma.start_transaction(
                        FESLService.MessageService,
                        FESLTransaction.AsyncPurgedEvent,
                        AsyncPurgedEvent(messageIds=[messageId]),
                    )

        return DeleteMessagesResponse()

    def __handle_purge_messages(
        self, data: PurgeMessagesRequest
    ) -> PurgeMessagesResponse:
        # Is this ever called from the client?
        raise NotImplementedError("PurgeMessages is not implemented.")

    def __create_async_message_event(
        self, request: AsyncMessageEvent
    ) -> AsyncMessageEvent:
        return request

    def __create_async_purged_event(
        self, request: AsyncPurgedEvent
    ) -> AsyncPurgedEvent:
        return request
