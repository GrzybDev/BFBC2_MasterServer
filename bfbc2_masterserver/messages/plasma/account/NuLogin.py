from typing import Optional

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuLoginRequest(PlasmaTransaction):
    returnEncryptedInfo: bool
    nuid: str
    password: str
    macAddr: str


class NuLoginResponse(PlasmaTransaction):
    nuid: str
    lkey: str
    profileId: str
    userId: str
    encryptedLoginInfo: Optional[str] = None
