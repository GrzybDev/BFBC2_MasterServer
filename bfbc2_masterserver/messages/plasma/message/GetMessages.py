from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GetMessagesRequest(PlasmaTransaction):
    attachmentTypes: list[str]
    box: str
    chunkSize: int


class GetMessagesResponse(PlasmaTransaction):
    messages: list[None]  # TODO
