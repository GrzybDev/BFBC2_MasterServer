from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class AsyncPurgedEvent(PlasmaTransaction):
    messageIds: list[int]
