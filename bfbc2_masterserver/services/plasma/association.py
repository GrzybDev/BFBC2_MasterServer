from typing import Tuple

from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.assocation.AddAssocations import (
    AddAssociationsRequest,
)
from bfbc2_masterserver.messages.plasma.assocation.GetAssociations import (
    GetAssociationsRequest,
    GetAssociationsResponse,
)
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Association import (
    AssociationRequest,
    AssociationReturn,
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

        self.resolvers[FESLTransaction.AddAssociations] = (
            self.__handle_add_associations,
            AddAssociationsRequest,
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
        assocations: list[Association] | ErrorCode = self.database.assocation_get(
            data.owner.id, data.type
        )

        persona = self.database.persona_get_by_id(data.owner.id)

        if isinstance(assocations, ErrorCode):
            return TransactionError(ErrorCode.PARAMETERS_ERROR)
        elif isinstance(persona, ErrorCode):
            return TransactionError(persona)

        members = [
            AssociationReturn(
                id=association.target.id,
                name=association.target.name,
                type=1,
                created=association.createdAt,
                modified=association.updatedAt,
            )
            for association in assocations
        ]

        response = GetAssociationsResponse(
            domainPartition=data.domainPartition,
            maxListSize=20 if data.type != AssocationType.PlasmaRecentPlayers else 100,
            members=members,
            owner=Owner(id=data.owner.id, name=persona.name, type=data.owner.type),
            type=data.type,
        )

        return response

    def __handle_add_associations(self, data: AddAssociationsRequest):
        # TODO
        return PlasmaTransaction()
