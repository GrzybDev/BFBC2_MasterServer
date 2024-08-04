from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.EnterGameResponse import (
    EnterGameHostResponse,
)
from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


def handle_enter_game_response(ctx: BaseTheaterHandler, data: EnterGameHostResponse):
    yield TheaterTransaction()
