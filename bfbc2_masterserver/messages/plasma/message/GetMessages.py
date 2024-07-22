from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.database.Message import Message


class GetMessagesRequest(PlasmaTransaction):
    attachmentTypes: list[str]
    box: str
    chunkSize: int


class GetMessagesResponse(PlasmaTransaction):
    messages: list[Message]
