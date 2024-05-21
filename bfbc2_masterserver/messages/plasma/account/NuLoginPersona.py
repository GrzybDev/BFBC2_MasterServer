from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuLoginPersonaRequest(PlasmaTransaction):
    name: str


class NuLoginPersonaResponse(PlasmaTransaction):
    lkey: str
    profileId: int
    userId: int
