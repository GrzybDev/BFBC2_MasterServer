from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Message import MessageResponse


class GetMessageAttachmentsRequest(PlasmaTransaction):
    messageId: int
    keys: list[str]


class GetMessageAttachmentsResponse(PlasmaTransaction):
    pass
