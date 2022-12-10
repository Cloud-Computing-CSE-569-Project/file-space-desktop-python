from enum import Enum


class SyncEvent(Enum):
    deleted = 1
    created = 2
    updated = 3
    none = 4
