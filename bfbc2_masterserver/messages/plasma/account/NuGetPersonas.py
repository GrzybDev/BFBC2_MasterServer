from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuGetPersonasRequest(PlasmaTransaction):
    namespace: str


class NuGetPersonasResponse(PlasmaTransaction):
    personas: list[str]
