from pydantic import SecretStr

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuEntitleGameRequest(PlasmaTransaction):
    key: str
    nuid: str
    password: SecretStr


class NuEntitleGameResponse(PlasmaTransaction):
    nuid: str
    lkey: str
    profileId: int
    userId: int
