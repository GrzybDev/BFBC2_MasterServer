from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuDisablePersonaRequest(PlasmaTransaction):
    name: str


class NuDisablePersonaResponse(PlasmaTransaction):
    pass
