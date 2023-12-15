from channels.layers import get_channel_layer
from django.core.cache import cache
from packaging import version

from BFBC2_MasterServer.consumer import BFBC2Consumer
from Plasma.enumerators.ClientLocale import ClientLocale
from Plasma.enumerators.ClientPlatform import ClientPlatform
from Theater.transactor import Transactor


class TheaterConsumer(BFBC2Consumer):
    prot = None  # Protocol Version
    prod = None  # Game ID
    vers = None  # Game Version
    plat = None  # Platform
    locale = None  # Locale
    sdkVersion = None  # SDK Version

    initialized = False
    transactor = None

    persona = None
    currentlyUpdating = False

    lkey = None
    pid = None

    lid = None
    gid = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transactor = Transactor(self)

    async def disconnect(self, code):
        await super().disconnect(code)

        if self.lid and self.gid:
            from Theater.models import Game

            cache.delete(f"gameSession:{self.gid}")
            cache.delete(f"queue:{self.gid}")
            cache.delete(f"nextServerPlayerID:{self.gid}")

            await Game.objects.delete_game(self.gid)

        cache.delete(f"theaterSession:{self.lkey}")

    async def receive(self, text_data=None, bytes_data=None):
        message = await super().receive(text_data, bytes_data)

        if message is None:
            return

        await self.transactor.finish(message)

    async def initialize(self, data):
        """Initialize connection"""

        self.prot = data["protocolVersion"]
        self.prod = data["product"]
        self.vers = version.parse(data["version"])
        self.plat = ClientPlatform(data["platform"])
        self.locale = ClientLocale(data["locale"])
        self.sdkVersion = version.parse(data["sdkVersion"])

        if self.prot != 2:
            self.logger.warning(
                f"Protocol version {self.prot} is not officially supported by this server emulator!"
            )

            await self.send(
                text_data=f"WARNING: Your protocol version ({self.prot}) is not officially supported by this server emulator, some features may not work properly. Please install latest supported game version by this server emulator (Which is 795745)"
            )

        if self.vers == version.parse("1.0") or self.vers == version.parse("2.0"):
            # 1.0 - Client, 2.0 - Server
            pass
        else:
            self.logger.warning(
                f"Game version {self.vers} is not officially supported by this server emulator!"
            )

            await self.send(
                text_data=f"WARNING: Your game version ({self.vers}) is not officially supported by this server emulator, some features may not work properly. Please install latest supported game version by this server emulator (Which is 795745)"
            )

        if self.sdkVersion != version.parse("5.1.2.0.0"):
            self.logger.warning(
                f"SDK version {self.sdkVersion} is not officially supported by this server emulator!"
            )

            await self.send(
                text_data=f"WARNING: SDK version ({self.sdkVersion}) is not officially supported by this server emulator, some features may not work properly. Please install latest supported game version by this server emulator (Which is 795745)"
            )

        self.initialized = True

    async def external_send(self, event):
        message = event["message"]
        await self.transactor.start(message["service"], message["data"])

    async def send_remote_message(self, target, serviceStr, data):
        active_session = cache.get(f"theaterSession:{target}")
        channel_layer = get_channel_layer()

        if active_session:
            await channel_layer.send(
                active_session,
                {
                    "type": "external.send",
                    "message": {
                        "service": serviceStr,
                        "data": data,
                    },
                },
            )
    
    async def send_remote_message_server(self, target, serviceStr, data):
        active_session = cache.get(f"gameSession:{target}")
        channel_layer = get_channel_layer()

        if active_session:
            await channel_layer.send(
                active_session,
                {
                    "type": "external.send",
                    "message": {
                        "service": serviceStr,
                        "data": data,
                    },
                },
            )
