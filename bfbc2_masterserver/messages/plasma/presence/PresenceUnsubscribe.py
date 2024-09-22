from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Presence import PresenceRequest, PresenceResponse


class PresenceUnsubscribeRequest(PlasmaTransaction):
    requests: list[PresenceRequest]


class PresenceUnsubscribeResponse(PlasmaTransaction):
    responses: list[PresenceResponse]
