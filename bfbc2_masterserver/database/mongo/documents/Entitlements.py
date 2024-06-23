from mongoengine import BooleanField, DateTimeField, Document, IntField, StringField


class Entitlements(Document):
    tag = StringField(required=True)

    grant_date = DateTimeField(required=True)
    termination_date = DateTimeField()

    group_name = StringField()
    product_id = StringField()

    version = IntField()

    is_game_entitlement = BooleanField(default=False)
