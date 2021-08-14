from discord.ext.commands import MissingPermissions, check, Context
from .Permission import Permission


def validate(a, b) -> bool:
    """Determines if a class is valid against another"""
    return a.__validate__(b)


def has_permissions(permission: Permission):
    def predicate(ctx: Context):
        user_permission = Permission.from_discord_permissions(
            guild=ctx.guild,
            channel=ctx.channel,
            permissions=ctx.channel.permissions_for(ctx.author)
        )

        if validate(permission, user_permission):
            return True

        raise MissingPermissions([])
    return check(predicate)
