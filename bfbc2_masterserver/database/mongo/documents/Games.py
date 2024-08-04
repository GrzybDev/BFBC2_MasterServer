from mongoengine import (
    BooleanField,
    Document,
    FloatField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)


class Games(Document):
    id = IntField(primary_key=True)
    lid = IntField()
    owner = ReferenceField("Accounts")

    name = StringField(max_length=64)

    addrIp = StringField(max_length=15)
    addrPort = IntField()

    joiningPlayers = IntField(default=0)
    queuedPlayers = IntField(default=0)
    activePlayers = IntField(default=0)
    maxPlayers = IntField(default=32)

    platform = StringField(max_length=16)
    joinMode = StringField(max_length=16)
    gameType = StringField(max_length=16)

    serverSoftcore = BooleanField(default=False)
    serverHardcore = BooleanField(default=False)
    serverHasPassword = BooleanField(default=False)
    serverPunkbuster = BooleanField(default=False)
    serverEA = BooleanField(default=False)

    serverVersion = StringField(max_length=16)
    clientVersion = StringField(max_length=16)

    gameLevel = StringField()
    gameMod = StringField()
    gameMode = StringField()
    gameSGUID = IntField()
    gameTime = StringField()
    gameHash = StringField()
    gameRegion = StringField(max_length=2)
    gamePublic = BooleanField(default=False)
    gameElo = IntField(default=1000)
    gameAutoBalance = BooleanField(default=False)
    gameBannerUrl = StringField()
    gameCrosshair = BooleanField(default=False)
    gameFriendlyFire = FloatField(default=False)
    gameKillCam = BooleanField(default=False)
    gameMiniMap = BooleanField(default=False)
    gameMiniMapSpotting = BooleanField(default=False)
    gameThirdPersonVehicleCameras = BooleanField(default=False)
    gameThreeDSpotting = BooleanField(default=False)

    numObservers = IntField(default=0)
    maxObservers = IntField(default=0)

    providerId = StringField()
    queueLength = IntField(default=0)
    punkbusterVersion = StringField()

    ugid = StringField()
    ekey = StringField()
    secret = StringField()

    playerData = ListField(StringField())
    serverDescriptions = ListField(StringField())
