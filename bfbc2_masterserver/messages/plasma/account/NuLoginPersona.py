from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuLoginPersonaRequest(PlasmaTransaction):
    name: str


class NuLoginPersonaResponse(PlasmaTransaction):
    lkey: str
    profileId: int
    userId: int
