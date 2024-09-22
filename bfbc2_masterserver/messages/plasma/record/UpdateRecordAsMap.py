from datetime import datetime

from bfbc2_masterserver.enumerators.plasma.RecordName import RecordName
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class UpdateRecordAsMapRequest(PlasmaTransaction):
    recordName: RecordName
    values: dict[str, str]


class UpdateRecordAsMapResponse(PlasmaTransaction):
    pass
