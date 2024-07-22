from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class GetLockerURLRequest(PlasmaTransaction):
    pass


class GetLockerURLResponse(PlasmaTransaction):
    url: str
