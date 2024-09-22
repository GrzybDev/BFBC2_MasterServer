from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Presence import PresenceRequest, PresenceResponse


class PresenceSubscribeRequest(PlasmaTransaction):
    requests: list[PresenceRequest]


class PresenceSubscribeResponse(PlasmaTransaction):
    responses: list[PresenceResponse]
