from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.LeaveGame import (
    LeaveGameRequest,
    LeaveGameResponse,
)


def handle_leave_game(ctx: BaseTheaterHandler, data: LeaveGameRequest):
    yield LeaveGameResponse(LID=data.LID, GID=data.GID)
