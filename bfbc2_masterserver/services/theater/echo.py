from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest, EchoResponse


def handle_echo(ctx, data: EchoRequest):
    ip, port = (ctx.ws.client.host, ctx.ws.client.port)

    response = EchoResponse(
        TXN="ECHO",
        IP=ip,
        PORT=port,
        ERR=0,
        TYPE=data.TYPE,
    )

    yield response
