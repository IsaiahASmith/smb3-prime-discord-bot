from enum import Enum


class PermissionID(Enum):
    """All the possible permissions that are possible to provide"""
    CHANNEL_GROUPS = 1
    REGISTER_CHANNEL_GROUP = 2
    REMOVE_CHANNEL_GROUP = 3
    REGISTER_CHANNEL = 4
    UNREGISTER_CHANNEL = 5
