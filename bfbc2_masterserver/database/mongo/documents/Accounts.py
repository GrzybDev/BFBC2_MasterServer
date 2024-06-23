from mongoengine import (
    PULL,
    BooleanField,
    Document,
    EmailField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)

from bfbc2_masterserver.database.mongo.documents.Entitlements import Entitlements
from bfbc2_masterserver.database.mongo.documents.Personas import Personas


class Accounts(Document):
    id = IntField(primary_key=True)

    nuid = EmailField(required=True, unique=True)
    password = StringField(required=True)

    globalOptin = BooleanField(required=False)
    thirdPartyOptin = BooleanField(required=False)

    parentalEmail = StringField(required=False)

    DOBDay = IntField(required=False)
    DOBMonth = IntField(required=False)
    DOBYear = IntField(required=False)

    zipCode = StringField(required=False)
    country = StringField(required=False)
    language = StringField(required=False)

    tosVersion = StringField(required=False)
    serviceAccount = BooleanField(required=False)

    entitlements = ListField(ReferenceField(Entitlements))
    personas = ListField(ReferenceField(Personas, reverse_delete_rule=PULL))
