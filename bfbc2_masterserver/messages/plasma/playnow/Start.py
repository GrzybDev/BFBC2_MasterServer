from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Partition import Partition
from bfbc2_masterserver.models.plasma.PlayerProps import PlayerProps


class StartRequest(PlasmaTransaction):
    partition: Partition
    debugLevel: str
    version: int
    players: list[PlayerProps]


class StartResponse(PlasmaTransaction):
    id: dict
