from typing import Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuXBL360LoginRequest(PlasmaTransaction):
    macAddr: str
    consoleId: str
    tosVersion: Optional[str]


class NuXBL360LoginResponse(PlasmaTransaction):
    pass
