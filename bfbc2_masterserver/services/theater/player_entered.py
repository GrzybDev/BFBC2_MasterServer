from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.PlayerEntered import (
    PlayerEnteredRequest,
    PlayerEnteredResponse,
)


def handle_player_entered(ctx: BaseTheaterHandler, data: PlayerEnteredRequest):
    yield PlayerEnteredResponse(PID=data.PID)
