from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)


class MessageAttachments(EmbeddedDocument):
    key = StringField(required=True)
    type = StringField(required=True)
    data = StringField(required=True)


class Messages(Document):
    attachments = EmbeddedDocumentListField(MessageAttachments)
    deliveryType = StringField(required=True)
    messageId = IntField(primary_key=True)
    messageType = StringField(required=True)
    purgeStrategy = StringField(required=True)
    sender = ReferenceField("Personas")
    receivers = ListField(ReferenceField("Personas"))
    timeSent = DateTimeField(required=True)
    expiration = DateTimeField(required=True)
