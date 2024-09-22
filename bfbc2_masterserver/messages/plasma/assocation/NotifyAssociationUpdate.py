from bfbc2_masterserver.enumerators.plasma.AssocationUpdateOperation import (
    AssocationUpdateOperation,
)
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Association import AssociationReturn
from bfbc2_masterserver.models.plasma.DomainPartition import DomainPartition
from bfbc2_masterserver.models.plasma.Owner import Owner


class NotifyAssociationUpdate(PlasmaTransaction):
    domainPartition: DomainPartition
    listSize: int
    member: AssociationReturn
    operation: AssocationUpdateOperation
    owner: Owner
    type: str
