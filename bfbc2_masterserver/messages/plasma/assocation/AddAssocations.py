from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.database.Association import AssocationRequest
from bfbc2_masterserver.models.plasma.DomainPartition import DomainPartition


class AddAssociationsRequest(PlasmaTransaction):
    domainPartition: DomainPartition
    type: AssocationType
    listFullBehavior: str
    addRequests: list[AssocationRequest]
