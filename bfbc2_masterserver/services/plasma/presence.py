import json
from base64 import b64decode, b64encode

from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLService import FESLService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.presence.AsyncPresenceStatusEvent import (
    AsyncPresenceStatusEvent,
)
from bfbc2_masterserver.messages.plasma.presence.PresenceSubscribe import (
    PresenceSubscribeRequest,
    PresenceSubscribeResponse,
)
from bfbc2_masterserver.messages.plasma.presence.PresenceUnsubscribe import (
    PresenceUnsubscribeRequest,
    PresenceUnsubscribeResponse,
)
from bfbc2_masterserver.messages.plasma.presence.SetPresenceStatus import (
    SetPresenceStatusRequest,
    SetPresenceStatusResponse,
)
from bfbc2_masterserver.models.plasma.Owner import Owner
from bfbc2_masterserver.models.plasma.Presence import PresenceResponse


class PresenceService(PlasmaService):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[FESLTransaction.SetPresenceStatus] = (
            self.__handle_set_presence_status,
            SetPresenceStatusRequest,
        )

        self.resolvers[FESLTransaction.PresenceSubscribe] = (
            self.__handle_presence_subscribe,
            PresenceSubscribeRequest,
        )

        self.resolvers[FESLTransaction.PresenceUnsubscribe] = (
            self.__handle_presence_unsubscribe,
            PresenceUnsubscribeRequest,
        )

        self.generators[FESLTransaction.AsyncPresenceStatusEvent] = (
            self.__create_async_presence_status_event
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

    def _get_generator(self, txn):  # -> Any:
        """
        Gets the generator for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The generator function for the transaction.
        """
        return self.generators[FESLTransaction(txn)]

    def __handle_set_presence_status(
        self, data: SetPresenceStatusRequest
    ) -> SetPresenceStatusResponse | TransactionError:
        status = json.dumps(data.status)
        statusEncoded = b64encode(status.encode("utf-8")).decode("utf-8")

        if not self.connection.persona:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        self.redis.set(f"presence:{self.connection.persona.id}", statusEncoded)
        return SetPresenceStatusResponse()

    def __handle_presence_subscribe(
        self, data: PresenceSubscribeRequest
    ) -> PresenceSubscribeResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SESSION_NOT_AUTHORIZED)

        responses = []

        for request in data.requests:
            owner = self.database.persona_get_by_id(request.userId)

            if isinstance(owner, ErrorCode):
                return TransactionError(owner)

            responses.append(
                PresenceResponse(
                    owner=Owner(id=owner.id, name=owner.name, type=0), outcome=0
                )
            )

            targetUserStatus = self.redis.get(f"presence:{request.userId}")
            accountId = self.database.persona_get_owner_id(owner.id)

            if isinstance(accountId, ErrorCode):
                return TransactionError(accountId)

            receiverSession = self.plasma.manager.CLIENTS.get(accountId)

            if targetUserStatus and receiverSession:
                self.plasma.start_transaction(
                    FESLService.PresenceService,
                    FESLTransaction.AsyncPresenceStatusEvent,
                    AsyncPresenceStatusEvent(
                        initial=True,
                        owner=Owner(id=owner.id, name=owner.name, type=0),
                        status=json.loads(str(b64decode(targetUserStatus).decode("utf-8"))),  # type: ignore
                    ),
                )

                receiverSession.plasma.start_transaction(
                    FESLService.PresenceService,
                    FESLTransaction.AsyncPresenceStatusEvent,
                    AsyncPresenceStatusEvent(
                        initial=True,
                        owner=Owner(
                            id=self.connection.persona.id,
                            name=self.connection.persona.name,
                            type=0,
                        ),
                        status=json.loads(str(b64decode(targetUserStatus).decode("utf-8"))),  # type: ignore
                    ),
                )

        return PresenceSubscribeResponse(responses=responses)

    def __handle_presence_unsubscribe(
        self, data: PresenceUnsubscribeRequest
    ) -> PresenceUnsubscribeResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SESSION_NOT_AUTHORIZED)

        responses = []

        for request in data.requests:
            owner = self.database.persona_get_by_id(request.userId)

            if isinstance(owner, ErrorCode):
                return TransactionError(owner)

            responses.append(
                PresenceResponse(
                    owner=Owner(id=owner.id, name=owner.name, type=0), outcome=0
                )
            )

        return PresenceUnsubscribeResponse(responses=responses)

    def __create_async_presence_status_event(
        self, request: AsyncPresenceStatusEvent
    ) -> AsyncPresenceStatusEvent:
        return request
