from typing import Optional

from pydantic import SecretStr

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuLoginRequest(PlasmaTransaction):
    returnEncryptedInfo: bool
    encryptedInfo: Optional[str] = None
    nuid: Optional[str] = None
    password: Optional[SecretStr] = None
    macAddr: str
    tosVersion: Optional[str] = None


class NuLoginResponse(PlasmaTransaction):
    nuid: str
    lkey: str
    profileId: int
    userId: int
    encryptedLoginInfo: Optional[str] = None
