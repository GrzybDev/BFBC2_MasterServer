from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.enumerators.plasma.ListFullBehavior import ListFullBehavior
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Association import (
    AssociationRequest,
    AssociationResult,
    AssociationReturn,
)
from bfbc2_masterserver.models.plasma.DomainPartition import DomainPartition
from bfbc2_masterserver.models.plasma.Owner import Owner


class DeleteAssociationsRequest(PlasmaTransaction):
    domainPartition: DomainPartition
    type: AssocationType
    deleteRequests: list[AssociationRequest]


class DeleteAssociationsResponse(PlasmaTransaction):
    domainPartition: DomainPartition
    maxListSize: int
    result: list[AssociationResult]
    type: AssocationType
