from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.messages.plasma.record.GetRecordAsMap import (
    GetRecordAsMapRequest,
    GetRecordAsMapResponse,
)
from bfbc2_masterserver.services.service import Service


class RecordService(Service):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[Transaction.GetRecordAsMap] = (
            self.__handle_get_record_as_map,
            GetRecordAsMapRequest,
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

    def __handle_get_record_as_map(self, data: GetRecordAsMapRequest):
        # TODO: Implement this
        return GetRecordAsMapResponse(state=1, TTL=0)
