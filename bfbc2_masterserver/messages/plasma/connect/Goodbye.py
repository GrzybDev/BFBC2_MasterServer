from email import message

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GoodbyeRequest(PlasmaTransaction):
    reason: str
    message: str
