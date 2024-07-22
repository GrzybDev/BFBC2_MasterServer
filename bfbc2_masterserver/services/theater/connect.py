from time import time

from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.Connect import (
    ConnectRequest,
    ConnectResponse,
)


def handle_connect(ctx: BaseTheaterHandler, data: ConnectRequest):
    if ctx.isInitialized:
        raise ValueError("Theater is already initialized")

    ctx.isInitialized = True

    response = ConnectResponse(
        TIME=int(time()),
        activityTimeoutSecs=240,
        PROT=data.PROT,
    )

    yield response
