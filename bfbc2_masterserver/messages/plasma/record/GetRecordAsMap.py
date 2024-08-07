from datetime import datetime

from bfbc2_masterserver.enumerators.plasma.RecordName import RecordName
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class GetRecordAsMapRequest(PlasmaTransaction):
    recordName: RecordName


class GetRecordAsMapResponse(PlasmaTransaction):
    state: int
    TTL: int
    values: dict[str, str]
    lastModified: datetime
