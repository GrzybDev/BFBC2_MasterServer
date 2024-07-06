from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.record.GetRecord import (
    GetRecordRequest,
    GetRecordResponse,
    Record,
)
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

        self.resolvers[Transaction.GetRecord] = (
            self.__handle_get_record,
            GetRecordRequest,
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
        records = self.database.get_records(self.plasma.userId, data.recordName)

        if not records:
            return TransactionError(ErrorCode.RECORD_NOT_FOUND)

        values = {record.key: record.value for record in records}
        return GetRecordAsMapResponse(
            state=1, TTL=0, lastModified=records[0].updated, values=values
        )

    def __handle_get_record(self, data: GetRecordRequest):
        records = self.database.get_records(self.plasma.userId, data.recordName)

        if not records:
            return TransactionError(ErrorCode.RECORD_NOT_FOUND)

        values = [Record(key=record.key, value=record.value) for record in records]
        return GetRecordResponse(values=values)
