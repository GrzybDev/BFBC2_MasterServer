from typing import Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuUpdatePasswordRequest(PlasmaTransaction):
    newPassword: str


class NuUpdatePasswordResponse(PlasmaTransaction):
    encryptedLoginInfo: Optional[str]
