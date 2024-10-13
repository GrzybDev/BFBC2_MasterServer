from enum import Enum


class MessageType(Enum):
    InitialError = 0x66657272
    PlasmaRequest = 0xC0000000
    PlasmaResponse = 0x80000000
    PlasmaChunkedRequest = 0xF0000000
    PlasmaChunkedResponse = 0xB0000000
    TheaterRequest = 0x40000000
    TheaterResponse = 0x00000000
    TheaterQueue = 0x71756575
