from bfbc2_masterserver.enumerators.plasma.RecordName import RecordName
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Record import Record


class GetRecordRequest(PlasmaTransaction):
    recordName: RecordName


class GetRecordResponse(PlasmaTransaction):
    values: list[Record]
