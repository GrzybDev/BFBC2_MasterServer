from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class SetPresenceStatusRequest(PlasmaTransaction):
    status: dict


class SetPresenceStatusResponse(PlasmaTransaction):
    pass
