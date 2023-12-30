from django.core.cache import cache

from BFBC2_MasterServer.packet import Packet


async def leave_game(connection, message):
    lid = message.Get("LID")
    gid = message.Get("GID")

    if connection.pid:
        queue_str = cache.get_or_set(f"queue:{gid}", "", timeout=None)
        queue_list = queue_str.split(";")

        try:
            queue_list.remove(str(connection.pid))
        except ValueError:
            # Server probably is shutdown and we cannot remove the player from the queue, ignore this exception
            pass

        cache.set(f"queue:{gid}", ";".join(queue_list), timeout=None)

    connection.pid = None

    response = Packet()
    response.Set("LID", lid)
    response.Set("GID", gid)

    yield response
