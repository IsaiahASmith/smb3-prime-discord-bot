from enum import Enum, auto


class PermissionID(Enum):
    """All the possible permissions that are possible to provide"""
    # Guild Wide Permissions
    ADMINISTRATOR = auto()
    MANAGE_EMOJIS = auto()
    VIEW_AUDIT_LOG = auto()
    VIEW_GUILD_INSIGHTS = auto()
    MANAGE_GUILD = auto()
    CHANGE_NICKNAME = auto()
    MANAGE_NICKNAMES = auto()
    KICK_MEMBERS = auto()
    BAN_MEMBERS = auto()
    CREATE_INSTANT_INVITE = auto()

    # Channel Permissions
    MANAGE_PERMISSIONS = auto()
    MANAGE_WEBHOOKS = auto()
    VIEW_CHANNEL = auto()

    # Text Channel Permissions
    MANAGE_MESSAGES = auto()
    MENTION_EVERYONE = auto()
    READ_MESSAGE_HISTORY = auto()
    READ_MESSAGES = auto()
    SEND_MESSAGES = auto()
    SEND_TTS_MESSAGES = auto()
    ADD_REACTIONS = auto()
    USE_EXTERNAL_EMOJIS = auto()
    ATTACH_FILES = auto()
    EMBED_LINKS = auto()
    USE_SLASH_COMMANDS = auto()
    REQUEST_TO_SPEAK = auto()

    # Voice Channel Permissions
    CONNECT = auto()
    SPEAK = auto()
    MUTE_MEMBERS = auto()
    DEAFEN_MEMBERS = auto()
    MOVE_MEMBERS = auto()
    USE_VOICE_ACTIVATION = auto()
    PRIORITY_SPEAKER = auto()
    STREAM = auto()

    # Channel Manager Permissions
    MANAGE_CHANNEL_GROUPS = auto()
    MANAGE_CHANNEL = auto()
