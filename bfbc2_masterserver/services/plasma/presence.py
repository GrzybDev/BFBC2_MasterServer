import json
from base64 import b64encode

from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.messages.plasma.presence.SetPresenceStatus import (
    SetPresenceStatusRequest,
    SetPresenceStatusResponse,
)
from bfbc2_masterserver.services.service import Service


class PresenceService(Service):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[Transaction.SetPresenceStatus] = (
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

    def __handle_set_presence_status(self, data: SetPresenceStatusRequest):
        status = json.dumps(data.status)
        statusEncoded = b64encode(status.encode("utf-8")).decode("utf-8")

        self.redis.set(f"presence:{self.plasma.userId}", statusEncoded)

        return SetPresenceStatusResponse()
