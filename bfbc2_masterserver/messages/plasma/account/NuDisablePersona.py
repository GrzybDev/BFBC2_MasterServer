from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuDisablePersonaRequest(PlasmaTransaction):
    name: str


class NuDisablePersonaResponse(PlasmaTransaction):
    pass
