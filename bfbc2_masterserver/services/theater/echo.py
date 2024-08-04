from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.Echo import EchoRequest, EchoResponse


def handle_echo(ctx: BaseTheaterHandler, data: EchoRequest):
    address = ctx.plasma.get_client_address()
    if not address:
        return

    ip, _ = address.split(":")

    response = EchoResponse(
        TXN="ECHO",
        IP=ip,
        PORT=ctx.plasma.connection.internalPort,
        ERR=0,
        TYPE=data.TYPE,
    )

    yield response
