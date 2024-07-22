from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.database.Association import Association
from bfbc2_masterserver.models.plasma.DomainPartition import DomainPartition
from bfbc2_masterserver.models.plasma.Owner import Owner


class GetAssociationsRequest(PlasmaTransaction):
    domainPartition: DomainPartition
    type: AssocationType
    owner: Owner


class GetAssociationsResponse(PlasmaTransaction):
    domainPartition: DomainPartition
    maxListSize: int
    members: list[Association]
    owner: Owner
    type: AssocationType
