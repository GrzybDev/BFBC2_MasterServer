from ast import Delete

from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLService import FESLService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.enumerators.plasma.AssocationUpdateOperation import (
    AssocationUpdateOperation,
)
from bfbc2_masterserver.enumerators.plasma.ListFullBehavior import ListFullBehavior
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.assocation.AddAssocations import (
    AddAssociationsRequest,
    AddAssociationsResponse,
)
from bfbc2_masterserver.messages.plasma.assocation.DeleteAssociations import (
    DeleteAssociationsRequest,
    DeleteAssociationsResponse,
)
from bfbc2_masterserver.messages.plasma.assocation.GetAssociations import (
    GetAssociationsRequest,
    GetAssociationsResponse,
)
from bfbc2_masterserver.messages.plasma.assocation.GetAssociationsCount import (
    GetAssociationsCountRequest,
)
from bfbc2_masterserver.messages.plasma.assocation.NotifyAssociationUpdate import (
    NotifyAssociationUpdate,
)
from bfbc2_masterserver.models.plasma.Association import (
    AssociationResult,
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

        self.resolvers[FESLTransaction.DeleteAssociations] = (
            self.__handle_delete_associations,
            DeleteAssociationsRequest,
        )

        self.resolvers[FESLTransaction.GetAssociationsCount] = (
            self.__handle_get_associations_count,
            GetAssociationsCountRequest,
        )

        self.generators[FESLTransaction.NotifyAssociationUpdate] = (
            self.__notify_association_update
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
        assocations: list[Association] | ErrorCode = self.database.association_get_all(
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
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SESSION_NOT_AUTHORIZED)

        maxAssociations = 20 if data.type != AssocationType.PlasmaRecentPlayers else 100
        result = []

        for addRequest in data.addRequests:
            outcome = 0

            associations = self.database.association_get_all(
                addRequest.owner.id, data.type
            )

            if isinstance(associations, ErrorCode):
                return TransactionError(ErrorCode.TRANSACTION_DATA_NOT_FOUND)

            isListFull = len(associations) >= maxAssociations

            if isListFull:
                if data.listFullBehavior == ListFullBehavior.ReturnError:
                    outcome = 23005
                elif (
                    data.listFullBehavior == ListFullBehavior.RollLeastRecentlyModified
                ):
                    # Order by oldest first
                    associations.sort(key=lambda x: x.updatedAt)
                    self.database.association_delete(associations[0].id)

            # Add new member
            assoResult = self.database.association_add(
                owner_id=addRequest.owner.id,
                target_id=addRequest.member.id,
                type=data.type,
            )

            if isinstance(assoResult, ErrorCode):
                outcome = 23005

            memberAccountId = self.database.persona_get_owner_id(addRequest.member.id)
            memberPersona = self.database.persona_get_by_id(addRequest.member.id)

            if isinstance(memberAccountId, ErrorCode) or isinstance(
                memberPersona, ErrorCode
            ):
                continue

            externalClient = self.plasma.manager.CLIENTS.get(memberAccountId)

            if externalClient:
                externalClient.plasma.start_transaction(
                    FESLService.AssociationService,
                    FESLTransaction.NotifyAssociationUpdate,
                    NotifyAssociationUpdate(
                        domainPartition=data.domainPartition,
                        listSize=len(associations) + 1,
                        member=AssociationReturn(
                            id=addRequest.owner.id,
                            name=self.connection.persona.name,
                            type=addRequest.owner.type,
                            created=(
                                assoResult.createdAt
                                if not isinstance(assoResult, ErrorCode)
                                else None
                            ),
                            modified=(
                                assoResult.updatedAt
                                if not isinstance(assoResult, ErrorCode)
                                else None
                            ),
                        ),
                        operation=AssocationUpdateOperation.ADD,
                        owner=Owner(
                            id=addRequest.member.id,
                            name=memberPersona.name,
                            type=addRequest.member.type,
                        ),
                        type=data.type.value,
                    ),
                )

            result.append(
                AssociationResult(
                    member=AssociationReturn(
                        id=addRequest.member.id,
                        name=memberPersona.name,
                        type=addRequest.member.type,
                        created=(
                            assoResult.createdAt
                            if not isinstance(assoResult, ErrorCode)
                            else None
                        ),
                        modified=(
                            assoResult.updatedAt
                            if not isinstance(assoResult, ErrorCode)
                            else None
                        ),
                    ),
                    owner=addRequest.owner,
                    mutual=data.type != AssocationType.PlasmaRecentPlayers,
                    outcome=outcome,
                    listSize=len(associations) + 1,
                )
            )

        response = AddAssociationsResponse(
            domainPartition=data.domainPartition,
            maxListSize=maxAssociations,
            result=result,
            type=data.type,
        )

        return response

    def __handle_delete_associations(self, data: DeleteAssociationsRequest):
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SESSION_NOT_AUTHORIZED)

        maxAssociations = 20 if data.type != AssocationType.PlasmaRecentPlayers else 100
        result = []

        for deleteRequest in data.deleteRequests:
            outcome = 0

            association = self.database.association_get(
                deleteRequest.owner.id, deleteRequest.member.id, data.type
            )

            associations = self.database.association_get_all(
                deleteRequest.owner.id, data.type
            )

            if isinstance(associations, ErrorCode):
                return TransactionError(ErrorCode.TRANSACTION_DATA_NOT_FOUND)

            if not association:
                outcome = 23005
            else:
                self.database.association_delete(association.id)

            memberAccountId = self.database.persona_get_owner_id(
                deleteRequest.member.id
            )
            memberPersona = self.database.persona_get_by_id(deleteRequest.member.id)

            if isinstance(memberAccountId, ErrorCode) or isinstance(
                memberPersona, ErrorCode
            ):
                continue

            externalClient = self.plasma.manager.CLIENTS.get(memberAccountId)

            if externalClient and association:
                externalClient.plasma.start_transaction(
                    FESLService.AssociationService,
                    FESLTransaction.NotifyAssociationUpdate,
                    NotifyAssociationUpdate(
                        domainPartition=data.domainPartition,
                        listSize=len(associations),
                        member=AssociationReturn(
                            id=deleteRequest.owner.id,
                            name=self.connection.persona.name,
                            type=1,
                            created=association.createdAt,
                            modified=association.updatedAt,
                        ),
                        operation=AssocationUpdateOperation.DEL,
                        owner=Owner(
                            id=deleteRequest.member.id,
                            name=deleteRequest.member.name,
                            type=deleteRequest.member.type,
                        ),
                        type=data.type.value,
                    ),
                )

            if association:
                result.append(
                    AssociationResult(
                        member=AssociationReturn(
                            id=deleteRequest.member.id,
                            name=memberPersona.name,
                            type=1,
                            created=association.createdAt,
                            modified=association.updatedAt,
                        ),
                        owner=deleteRequest.owner,
                        mutual=data.type != AssocationType.PlasmaRecentPlayers,
                        outcome=outcome,
                        listSize=len(associations),
                    )
                )

        response = DeleteAssociationsResponse(
            domainPartition=data.domainPartition,
            maxListSize=maxAssociations,
            result=result,
            type=data.type,
        )

        return response

    def __notify_association_update(self, data: NotifyAssociationUpdate):
        return data

    def __handle_get_associations_count(self, data: GetAssociationsCountRequest):
        associations = self.database.association_get_all(data.owner.id, data.type)

        if isinstance(associations, ErrorCode):
            return TransactionError(ErrorCode.TRANSACTION_DATA_NOT_FOUND)

        return len(associations)
