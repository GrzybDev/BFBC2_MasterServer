from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest, EchoResponse
from bfbc2_masterserver.messages.theater.commands.UpdateBracket import (
    UpdateBracketRequest,
    UpdateBracketResponse,
)


def handle_update_bracket(ctx, data: UpdateBracketRequest):
    ctx.update_in_progress = data.START

    yield UpdateBracketResponse()
