from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GetRecordAsMapRequest(PlasmaTransaction):
    recordName: str


class GetRecordAsMapResponse(PlasmaTransaction):
    state: int
    TTL: int
