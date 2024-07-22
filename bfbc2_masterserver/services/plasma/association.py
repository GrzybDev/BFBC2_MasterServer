from typing import Tuple

from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.assocation.GetAssociations import (
    GetAssociationsRequest,
    GetAssociationsResponse,
)
from bfbc2_masterserver.models.plasma.database.Association import Association
from bfbc2_masterserver.models.plasma.Owner import Owner


class AssociationService(PlasmaService):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[FESLTransaction.GetAssociations] = (
            self.__handle_get_associations,
            GetAssociationsRequest,
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

    def __handle_get_associations(
        self, data: GetAssociationsRequest
    ) -> GetAssociationsResponse | TransactionError:
        databaseAssocations: Tuple[str, list[Association]] | ErrorCode = (
            self.database.get_assocation(data.owner.id, data.type)
        )

        if not databaseAssocations or isinstance(databaseAssocations, ErrorCode):
            return TransactionError(ErrorCode.PARAMETERS_ERROR)

        persona_name, assocations = databaseAssocations

        response = GetAssociationsResponse(
            domainPartition=data.domainPartition,
            maxListSize=20 if data.type != AssocationType.PlasmaRecentPlayers else 100,
            members=assocations,
            owner=Owner(id=data.owner.id, name=persona_name, type=data.owner.type),
            type=data.type,
        )

        return response
