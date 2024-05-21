from typing import Optional

from pydantic import SecretStr

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuLoginRequest(PlasmaTransaction):
    returnEncryptedInfo: bool
    nuid: str
    password: SecretStr
    macAddr: str
    tosVersion: Optional[str] = None


class NuLoginResponse(PlasmaTransaction):
    nuid: str
    lkey: str
    profileId: str
    userId: str
    encryptedLoginInfo: Optional[str] = None
