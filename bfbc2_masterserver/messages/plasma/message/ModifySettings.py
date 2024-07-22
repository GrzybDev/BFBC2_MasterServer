from typing import Any, Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class ModifySettingsRequest(PlasmaTransaction):
    retrieveAttachmentTypes: list[Any]
    retrieveMessageTypes: Optional[list[Any]] = None
    notifyMessages: int


class ModifySettingsResponse(PlasmaTransaction):
    pass
