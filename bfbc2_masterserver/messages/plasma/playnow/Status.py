from typing import Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class StatusRequest(PlasmaTransaction):
    id: int
    gid: Optional[int] = None
    lid: Optional[int] = None


class StatusResponse(PlasmaTransaction):
    id: dict
    props: dict
    sessionState: str
