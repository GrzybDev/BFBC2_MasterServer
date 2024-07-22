from mongoengine import (
    DateTimeField,
    Document,
    EnumField,
    FloatField,
    IntField,
    QuerySet,
)

from bfbc2_masterserver.messages.plasma.record.GetRecord import RecordName


class Records(Document):
    persona_id = IntField(required=True)
    name = EnumField(RecordName)
    key = IntField(required=True)
    value = FloatField(required=True)
    updated = DateTimeField(required=True)
