from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Message import MessageResponse


class GetMessagesRequest(PlasmaTransaction):
    attachmentTypes: list[str]
    box: str
    chunkSize: int


class GetMessagesResponse(PlasmaTransaction):
    messages: list[MessageResponse]
