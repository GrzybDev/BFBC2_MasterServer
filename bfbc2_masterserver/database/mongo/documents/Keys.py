from mongoengine import (
    BooleanField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    QuerySet,
    StringField,
)


class Targets(EmbeddedDocument):
    tag = StringField(required=True)
    group = StringField()
    product = StringField()
    isGameEntitlement = BooleanField()


class Keys(Document):
    key = StringField(primary_key=True)
    targets = EmbeddedDocumentListField(Targets)

    active = BooleanField(default=True)
    consumable = BooleanField(default=True)
