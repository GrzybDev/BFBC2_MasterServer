from time import time

from bfbc2_masterserver.messages.theater.commands.Connect import (
    ConnectRequest,
    ConnectResponse,
)


def handle_connect(ctx, data: ConnectRequest):
    if ctx.initialized:
        raise ValueError("Theater is already initialized")

    ctx.initialized = True

    response = ConnectResponse(
        TIME=int(time()),
        activityTimeoutSecs=240,
        PROT=data.PROT,
    )

    yield response
