from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Owner import Owner


class AsyncPresenceStatusEvent(PlasmaTransaction):
    initial: bool
    owner: Owner
    status: dict
