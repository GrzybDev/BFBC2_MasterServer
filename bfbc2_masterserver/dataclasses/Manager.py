from redis import Redis
from bfbc2_masterserver.database import DatabaseAPI
from bfbc2_masterserver.dataclasses.Client import Client


class BaseManager:
    CLIENTS: dict[int, Client] = {}
    SERVERS: dict[int, Client] = {}

    database: DatabaseAPI
    redis: Redis
