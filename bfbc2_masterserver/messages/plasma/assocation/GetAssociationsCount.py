from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Association import AssociationReturn
from bfbc2_masterserver.models.plasma.DomainPartition import DomainPartition
from bfbc2_masterserver.models.plasma.Owner import Owner


class GetAssociationsCountRequest(PlasmaTransaction):
    domainPartition: DomainPartition
    type: AssocationType
    owner: Owner


class GetAssociationsCountResponse(PlasmaTransaction):
    domainPartition: DomainPartition
    maxListSize: int
    count: int
    owner: Owner
