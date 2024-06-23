from datetime import datetime

from mongoengine import (
    PULL,
    DateTimeField,
    Document,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)


class Personas(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True, unique=True)

    blocked = ListField(ReferenceField("Personas", reverse_delete_rule=PULL))
    friends = ListField(ReferenceField("Personas", reverse_delete_rule=PULL))
    muted = ListField(ReferenceField("Personas", reverse_delete_rule=PULL))
    recent = ListField(ReferenceField("Personas", reverse_delete_rule=PULL))

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
