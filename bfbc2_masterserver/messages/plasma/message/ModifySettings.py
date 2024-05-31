from typing import Any

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class ModifySettingsRequest(PlasmaTransaction):
    retrieveAttachmentTypes: list[Any]
    notifyMessages: int


class ModifySettingsResponse(PlasmaTransaction):
    pass
