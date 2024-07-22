from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest, EchoResponse
from bfbc2_masterserver.messages.theater.commands.UpdateBracket import (
    UpdateBracketRequest,
    UpdateBracketResponse,
)


def handle_update_bracket(ctx: BaseTheaterHandler, data: UpdateBracketRequest):
    ctx.updateInProgress = data.START

    yield UpdateBracketResponse()
