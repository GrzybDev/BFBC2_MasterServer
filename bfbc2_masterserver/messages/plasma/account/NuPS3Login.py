from typing import Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuPS3LoginRequest(PlasmaTransaction):
    ticket: bytes
    macAddr: str
    consoleId: str
    tosVersion: Optional[str]


class NuPS3LoginResponse(PlasmaTransaction):
    pass
