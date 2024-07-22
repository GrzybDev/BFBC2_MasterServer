from typing import Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class GoodbyeRequest(PlasmaTransaction):
    reason: str | int
    message: Optional[str] = None
