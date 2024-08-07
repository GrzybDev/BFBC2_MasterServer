import json
from base64 import b64encode

from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.presence.SetPresenceStatus import (
    SetPresenceStatusRequest,
    SetPresenceStatusResponse,
)


class PresenceService(PlasmaService):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[FESLTransaction.SetPresenceStatus] = (
            self.__handle_set_presence_status,
            SetPresenceStatusRequest,
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

        self.plasma.manager.redis.set(
            f"presence:{self.connection.persona.id}", statusEncoded
        )

        return SetPresenceStatusResponse()
