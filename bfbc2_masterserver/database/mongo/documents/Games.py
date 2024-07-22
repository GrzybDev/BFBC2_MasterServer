from mongoengine import Document, IntField, ListField, QuerySet, StringField


class Games(Document):
    id = IntField(primary_key=True)
    lid = IntField()

    name = StringField(max_length=64, unique=True)

    addrIp = StringField(max_length=15)
    addrPort = IntField()

    joiningPlayers = IntField(default=0)
    queuedPlayers = IntField(default=0)
    activePlayers = IntField(default=0)
    maxPlayers = IntField(default=32)

    platform = StringField(max_length=16)
    joinMode = StringField(max_length=16)
    gameType = StringField(max_length=16)

    serverSoftcore = IntField(default=False)
    serverHardcore = IntField(default=False)
    serverHasPassword = IntField(default=False)
    serverPunkbuster = IntField(default=False)
    serverEA = IntField(default=False)

    serverVersion = StringField(max_length=16)
    clientVersion = StringField(max_length=16)

    gameLevel = StringField()
    gameMod = StringField()
    gameMode = StringField()
    gameSGUID = IntField()
    gameTime = StringField()
    gameHash = StringField()
    gameRegion = StringField(max_length=2)
    gamePublic = IntField(default=False)
    gameElo = IntField(default=1000)
    gameAutoBalance = IntField(default=False)
    gameBannerUrl = StringField()
    gameCrosshair = IntField(default=False)
    gameFriendlyFire = IntField(default=False)
    gameKillCam = IntField(default=False)
    gameMiniMap = IntField(default=False)
    gameMiniMapSpotting = IntField(default=False)
    gameThirdPersonVehicleCameras = IntField(default=False)
    gameThreeDSpotting = IntField(default=False)

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
