from enum import Enum


class Transaction(Enum):
    # Plasma (Connect)
    Hello = "Hello"
    MemCheck = "MemCheck"
    Ping = "Ping"
    Goodbye = "Goodbye"
    Suicide = "Suicide"
    GetPingSites = "GetPingSites"
