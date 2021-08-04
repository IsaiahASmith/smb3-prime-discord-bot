from typing import Optional

from discord.ext.commands import Converter, Context

from Permissions import Permission, PermissionID

_permission_codes = {
    "cg": PermissionID.CHANNEL_GROUPS,
    "channel_groups": PermissionID.CHANNEL_GROUPS,
    "rcg": PermissionID.REGISTER_CHANNEL_GROUP,
    "register_channel_group": PermissionID.REGISTER_CHANNEL_GROUP,
    "rem_cg": PermissionID.REMOVE_CHANNEL_GROUP,
    "remove_channel_group": PermissionID.REMOVE_CHANNEL_GROUP,
    "rc": PermissionID.REGISTER_CHANNEL,
    "register_channel": PermissionID.REGISTER_CHANNEL,
    "uc": PermissionID.UNREGISTER_CHANNEL,
    "unregister_channel": PermissionID.UNREGISTER_CHANNEL
}


def get_permission(name: str) -> Optional[PermissionID]:
    name = name.lower()
    if name in _permission_codes:
        return _permission_codes[name]


class PermissionConverter(Converter):
    """Tries and finds a valid Permission"""
    async def convert(self, ctx: Context, argument: str) -> Optional[Permission]:
        return Permission(guild=ctx.guild, permissions={get_permission(perm) for perm in argument.split(',')})
