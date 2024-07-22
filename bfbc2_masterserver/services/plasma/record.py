from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.record.GetRecord import (
    GetRecordRequest,
    GetRecordResponse,
)
from bfbc2_masterserver.messages.plasma.record.GetRecordAsMap import (
    GetRecordAsMapRequest,
    GetRecordAsMapResponse,
)
from bfbc2_masterserver.models.plasma.database.Record import Record


class RecordService(PlasmaService):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[FESLTransaction.GetRecordAsMap] = (
            self.__handle_get_record_as_map,
            GetRecordAsMapRequest,
        )

        self.resolvers[FESLTransaction.GetRecord] = (
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

    def __handle_get_record_as_map(
        self, data: GetRecordAsMapRequest
    ) -> GetRecordAsMapResponse | TransactionError:
        records = self.database.get_records(
            self.plasma.connection.personaId, data.recordName
        )

        if not records:
            return TransactionError(ErrorCode.RECORD_NOT_FOUND)

        values = {record.key: record.value for record in records}
        return GetRecordAsMapResponse(
            state=1, TTL=0, lastModified=records[0].updated, values=values
        )

    def __handle_get_record(
        self, data: GetRecordRequest
    ) -> GetRecordResponse | TransactionError:
        records = self.database.get_records(
            self.plasma.connection.personaId, data.recordName
        )

        if not records:
            return TransactionError(ErrorCode.RECORD_NOT_FOUND)

        values = [Record(key=record.key, value=record.value) for record in records]
        return GetRecordResponse(values=values)
