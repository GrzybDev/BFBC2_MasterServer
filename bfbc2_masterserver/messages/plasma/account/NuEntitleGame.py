from typing import Optional

from pydantic import SecretStr

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuEntitleGameRequest(PlasmaTransaction):
    key: str
    encryptedInfo: Optional[str] = None
    nuid: Optional[str] = None
    password: Optional[SecretStr] = None


class NuEntitleGameResponse(PlasmaTransaction):
    nuid: str
    lkey: str
    profileId: int
    userId: int
