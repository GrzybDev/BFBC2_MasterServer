from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuGetPersonasRequest(PlasmaTransaction):
    namespace: str


class NuGetPersonasResponse(PlasmaTransaction):
    personas: list[str]
