from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.messages.plasma.Association import Association
from bfbc2_masterserver.messages.plasma.DomainPartition import DomainPartition
from bfbc2_masterserver.messages.plasma.Owner import Owner
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


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
