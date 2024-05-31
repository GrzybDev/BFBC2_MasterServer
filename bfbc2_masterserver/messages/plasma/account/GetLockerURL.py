from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GetLockerURLRequest(PlasmaTransaction):
    pass


class GetLockerURLResponse(PlasmaTransaction):
    url: str
