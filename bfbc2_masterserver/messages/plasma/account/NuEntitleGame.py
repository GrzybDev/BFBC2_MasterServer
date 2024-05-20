from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuEntitleGameRequest(PlasmaTransaction):
    key: str
    nuid: str
    password: str
