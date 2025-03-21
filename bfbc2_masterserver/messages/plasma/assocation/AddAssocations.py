from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.enumerators.plasma.ListFullBehavior import ListFullBehavior
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Association import (
    AssociationRequest,
    AssociationResult,
)
from bfbc2_masterserver.models.plasma.DomainPartition import DomainPartition


class AddAssociationsRequest(PlasmaTransaction):
    domainPartition: DomainPartition
    type: AssocationType
    listFullBehavior: ListFullBehavior
    addRequests: list[AssociationRequest]


class AddAssociationsResponse(PlasmaTransaction):
    domainPartition: DomainPartition
    maxListSize: int
    result: list[AssociationResult]
    type: AssocationType
