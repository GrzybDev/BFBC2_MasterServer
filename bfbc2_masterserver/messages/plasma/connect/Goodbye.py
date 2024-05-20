from typing import Optional

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GoodbyeRequest(PlasmaTransaction):
    reason: str
    message: Optional[str] = None
