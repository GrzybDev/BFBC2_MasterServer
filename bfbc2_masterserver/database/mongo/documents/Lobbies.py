from mongoengine import Document, IntField, StringField


class Lobbies(Document):
    id = IntField(primary_key=True)
    name = StringField(max_length=64, unique=True)
    locale = StringField(max_length=5)
    maxGames = IntField(default=10000)
