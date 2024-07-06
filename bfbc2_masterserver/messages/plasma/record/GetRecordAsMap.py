from datetime import datetime

from bfbc2_masterserver.enumerators.RecordName import RecordName
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GetRecordAsMapRequest(PlasmaTransaction):
    recordName: RecordName


class GetRecordAsMapResponse(PlasmaTransaction):
    state: int
    TTL: int
    values: dict[int, str]
    lastModified: datetime
