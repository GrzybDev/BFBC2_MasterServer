from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.record.AddRecord import (
    AddRecordRequest,
    AddRecordResponse,
)
from bfbc2_masterserver.messages.plasma.record.AddRecordAsMap import (
    AddRecordAsMapRequest,
    AddRecordAsMapResponse,
)
from bfbc2_masterserver.messages.plasma.record.GetRecord import (
    GetRecordRequest,
    GetRecordResponse,
)
from bfbc2_masterserver.messages.plasma.record.GetRecordAsMap import (
    GetRecordAsMapRequest,
    GetRecordAsMapResponse,
)
from bfbc2_masterserver.messages.plasma.record.UpdateRecord import (
    UpdateRecordRequest,
    UpdateRecordResponse,
)
from bfbc2_masterserver.messages.plasma.record.UpdateRecordAsMap import (
    UpdateRecordAsMapRequest,
    UpdateRecordAsMapResponse,
)
from bfbc2_masterserver.models.plasma.Record import Record


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

        self.resolvers[FESLTransaction.AddRecord] = (
            self.__handle_add_record,
            AddRecordRequest,
        )

        self.resolvers[FESLTransaction.UpdateRecord] = (
            self.__handle_update_record,
            UpdateRecordRequest,
        )

        self.resolvers[FESLTransaction.AddRecordAsMap] = (
            self.__handle_add_record_as_map,
            AddRecordAsMapRequest,
        )

        self.resolvers[FESLTransaction.UpdateRecordAsMap] = (
            self.__handle_update_record_as_map,
            UpdateRecordAsMapRequest,
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
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        records = self.database.record_get(self.connection.persona.id, data.recordName)

        if not records:
            return TransactionError(ErrorCode.RECORD_NOT_FOUND)

        values = {"{" + str(record.key) + "}": record.value for record in records}
        return GetRecordAsMapResponse(
            state=1,
            TTL=0,
            lastModified=max(record.updatedAt for record in records),
            values=values,
        )

    def __handle_get_record(
        self, data: GetRecordRequest
    ) -> GetRecordResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        records = self.database.record_get(self.connection.persona.id, data.recordName)

        if not records:
            return TransactionError(ErrorCode.RECORD_NOT_FOUND)

        values = [Record(key=record.key, value=record.value) for record in records]
        return GetRecordResponse(values=values)

    def __handle_add_record(
        self, data: AddRecordRequest
    ) -> AddRecordResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        for record in data.values:
            self.database.record_add(
                self.connection.persona.id, data.recordName, record.key, record.value
            )

        return AddRecordResponse()

    def __handle_update_record(
        self, data: UpdateRecordRequest
    ) -> UpdateRecordResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        for record in data.values:
            self.database.record_update(
                self.connection.persona.id, data.recordName, record.key, record.value
            )

        return UpdateRecordResponse()

    def __handle_add_record_as_map(
        self, data: AddRecordAsMapRequest
    ) -> AddRecordAsMapResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        for key, value in data.values.items():
            key = int(key[1:-1])  # Remove curly braces
            self.database.record_add(
                self.connection.persona.id, data.recordName, key, value
            )

        return AddRecordAsMapResponse()

    def __handle_update_record_as_map(
        self, data: UpdateRecordAsMapRequest
    ) -> UpdateRecordAsMapResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        for key, value in data.values.items():
            key = int(key[1:-1])  # Remove curly braces

            self.database.record_update(
                self.connection.persona.id, data.recordName, key, value
            )

        return UpdateRecordAsMapResponse()
