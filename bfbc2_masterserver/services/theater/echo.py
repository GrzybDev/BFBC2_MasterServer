from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest, EchoResponse


def handle_echo(ctx: BaseTheaterHandler, data: EchoRequest):
    if ctx.websocket.client:
        ip, port = (ctx.websocket.client.host, ctx.websocket.client.port)
    else:
        ip, port = ("127.0.0.1", 12345)

    response = EchoResponse(
        TXN="ECHO",
        IP=ip,
        PORT=port,
        ERR=0,
        TYPE=data.TYPE,
    )

    yield response
