from typing import Optional, Dict, Set
from asyncio import TimeoutError as AsyncTimeoutError
from functools import partialmethod

from discord import Member, Message, TextChannel, Guild
from discord.ext.commands import Cog, command, has_permissions, Greedy, Context, MissingPermissions, check
from perm_banana import Permission

from Security.Permission import Hole, TokenInvalidatedException
from converters.PermissionConverter import PermissionConverter as PermConverter


def validate(a, b) -> bool:
    """Determines if a class is valid against another"""
    return a.__validate__(b)


class PasswordTimeout(Exception):
    def __init__(self, message="Failed to create a password before timeout"):
        super().__init__(message)


class Security(Cog):
    _id_count = 0

    def __init__(self, bot):
        self.bot = bot
        self._pending_holes: Dict[int, Hole] = {}

    def get_holes(
        self, member: Optional[Member] = None, channel: Optional[TextChannel] = None, guild: Optional[Guild] = None
    ) -> Set[Hole]:
        """Fines a hole with a given set of information"""
        holes = set()
        for hole in self._pending_holes.values():
            if member is not None and member not in hole.members:
                continue
            if channel is not None and channel != hole.permissions.channel:
                continue
            if guild is not None and guild != hole.permissions.guild:
                continue
            holes.add(hole)
        return holes

    def validate_permissions(self, permission: Permission, ctx: Context):
        """Determines if a user has permissions from a context"""
        user_perms = Permission.from_discord_permissions(
            guild=ctx.guild, channel=ctx.channel, permissions=ctx.channel.permissions_for(ctx.author)
        )

        if validate(permission, user_perms):
            return True

        holes = self.get_holes(ctx.author, ctx.channel, ctx.guild)
        temp_perms = sum(hole.permissions for hole in holes)
        if validate(permission, user_perms + temp_perms):
            for hole in holes:
                hole.use(ctx.author)
            return True
        raise MissingPermissions([])

    def has_permission(self, permission: Permission):
        """Returns a check that validates if a user has a series of permissions"""
        return check(partialmethod(self.validate_permissions, permission))

    def open_hole(self, hole: Hole, duration: int) -> int:
        """Provides an id to check against"""
        hole_id = self._id_count
        self._pending_holes.update({self._id_count: hole})
        self.bot.scheduler.add_job(lambda hid=hole_id, *_: self.close_hole(hid), seconds=duration)
        self._id_count += 1
        return hole_id

    def close_hole(self, hole_id: int):
        """Removes a hole the check against"""
        del self._pending_holes[hole_id]

    def get_token_content(self, hole_id: int, member: Optional[Member] = None, password: Optional[str] = None):
        """Gets the content of a hole"""
        if hole_id not in self._pending_holes:
            raise TokenInvalidatedException(None, "Invalid Token - None found")

        return self._pending_holes[hole_id].get_content(member, password)

    async def ask_user_for_password(self, author: Member, channel: TextChannel, password: str = ""):
        """Asks the user for a password"""

        def password_check(message: Message) -> bool:
            if author != message.author:
                return False
            nonlocal password
            password = message.content
            await message.channel.send(f"The password is: {password}")
            return True

        await channel.send("DM me your password")
        try:
            await self.bot.wait_for("direct_message", timeout=60.0, check=password_check)
        except AsyncTimeoutError:
            await channel.send("Timeout")
            raise PasswordTimeout()

    async def generate_token_password(self, ctx: Context, author: Optional[Member] = None) -> str:
        """Asks the member for a password"""
        author = ctx.author if author is None else author
        return await self.ask_user_for_password(author, ctx.channel)

    @command(name="generate_token", aliases=["gt"])
    @has_permissions(manage_guild=True)
    async def generate_token(
        self, ctx, permissions: PermConverter, members: Optional[Greedy[Member]], uses: int = 1, duration: int = 60.0
    ):
        if members is not None:
            members = set(members)
        password = None if members is not None else await self.generate_token_password(ctx)
        hole = Hole.from_password(permissions, uses, members, password)
        return self.open_hole(hole, duration)


def setup(bot):
    cog = Security(bot)
    bot.add_cog(cog)
    return cog
