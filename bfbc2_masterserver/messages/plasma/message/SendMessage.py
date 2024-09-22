from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Attachment import Attachment
from bfbc2_masterserver.models.plasma.Status import Status


class SendMessageRequest(PlasmaTransaction):
    attachments: list[Attachment]
    to: list[int]
    expires: int
    deliveryType: str
    messageType: str
    purgeStrategy: str


class SendMessageResponse(PlasmaTransaction):
    messageId: int
    status: list[Status]
