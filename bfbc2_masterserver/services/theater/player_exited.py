from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.PlayerExited import (
    PlayerExitedRequest,
    PlayerExitedResponse,
)


def handle_player_exited(ctx: BaseTheaterHandler, data: PlayerExitedRequest):
    yield PlayerExitedResponse()
