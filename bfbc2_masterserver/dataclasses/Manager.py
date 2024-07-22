from redis import Redis

from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.dataclasses.Client import Client


class BaseManager:
    CLIENTS: dict[int, Client] = {}
    SERVERS: dict[int, Client] = {}

    database: BaseDatabase
    redis: Redis
