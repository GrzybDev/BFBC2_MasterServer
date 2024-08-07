from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest, EchoResponse


def handle_echo(ctx: BaseTheaterHandler, data: EchoRequest):
    address = ctx.client.plasma.get_client_address()

    if not address or not ctx.client.connection.internalPort:
        return

    response = EchoResponse(
        TXN="ECHO",
        IP=address[0],
        PORT=ctx.client.connection.internalPort,
        ERR=0,
        TYPE=data.TYPE,
    )

    yield response
