from enum import Enum


class ListFullBehavior(Enum):
    ReturnError = "ReturnError"
    RollLeastRecentlyModified = "RollLeastRecentlyModified"
