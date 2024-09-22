from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Message import MessageResponse


class AsyncMessageEvent(PlasmaTransaction, MessageResponse):
    pass
