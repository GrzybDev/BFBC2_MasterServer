from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class SetPresenceStatusRequest(PlasmaTransaction):
    status: dict


class SetPresenceStatusResponse(PlasmaTransaction):
    pass
