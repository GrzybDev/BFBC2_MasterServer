from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.assocation.GetAssociations import (
    GetAssocationsResponse,
    GetAssociationsRequest,
)
from bfbc2_masterserver.messages.plasma.Owner import Owner
from bfbc2_masterserver.services.service import Service


class AssociationService(Service):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[Transaction.GetAssociations] = (
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

    def __handle_get_associations(self, data: GetAssociationsRequest):
        assocations = self.database.get_assocation(data.owner.id, data.type)

        if not assocations or isinstance(assocations, ErrorCode):
            return TransactionError(ErrorCode.PARAMETERS_ERROR)

        persona_name, assocations = assocations

        response = GetAssocationsResponse(
            domainPartition=data.domainPartition,
            maxListSize=20 if data.type != AssocationType.PlasmaRecentPlayers else 100,
            members=assocations,
            owner=Owner(id=data.owner.id, name=persona_name, type=data.owner.type),
            type=data.type,
        )

        return response
