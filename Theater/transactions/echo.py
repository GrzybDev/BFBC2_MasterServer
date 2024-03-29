from BFBC2_MasterServer.packet import Packet


def echo(connection, message):
    """Handle echo transaction"""

    _, port = connection.scope["client"]

    response = Packet()
    response.Set("TXN", message.service)
    response.Set("IP", connection.ip)
    response.Set("PORT", port)
    response.Set("ERR", 0)
    response.Set("TYPE", 1)
    response.Set("TID", message.Get("TID"))

    yield response
