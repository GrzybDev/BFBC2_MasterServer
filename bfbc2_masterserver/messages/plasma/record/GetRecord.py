from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GetRecordRequest(PlasmaTransaction):
    recordName: str


class GetRecordResponse(PlasmaTransaction):
    pass
