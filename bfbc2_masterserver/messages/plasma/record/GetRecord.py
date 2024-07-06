from enum import Enum

from bfbc2_masterserver.enumerators.RecordName import RecordName
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class Record(PlasmaTransaction):
    key: int
    value: str


class GetRecordRequest(PlasmaTransaction):
    recordName: RecordName


class GetRecordResponse(PlasmaTransaction):
    values: list[Record]
