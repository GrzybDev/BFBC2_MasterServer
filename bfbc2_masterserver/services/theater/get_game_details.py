from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.GetGameDetails import (
    GetGameDetailsRequest,
    GetGameDetailsResponse,
)


def handle_get_game_details(ctx: BaseTheaterHandler, data: GetGameDetailsRequest):
    yield GetGameDetailsResponse()
