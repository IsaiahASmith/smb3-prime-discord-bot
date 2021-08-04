from typing import Optional, Dict
from asyncio import TimeoutError as AsyncTimeoutError

from discord import Member, DMChannel, Message
from discord.ext.commands import Cog, command, has_permissions, Greedy

from Permissions import Hole, TokenInvalidatedException
from converters.PermissionConverter import PermissionConverter


class PasswordTimeout(Exception):
    def __init__(self, message="Failed to create a password before timeout"):
        super().__init__(message)


class Security(Cog):
    _id_count = 0

    def __init__(self, bot):
        self.bot = bot
        self._pending_holes: Dict[int, Hole] = {}

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

    async def generate_token_password(self, ctx, author: Optional[Member] = None) -> str:
        """Asks the member for a password"""
        if author is None:
            author = ctx.author

        password = ""

        def check(message: Message) -> bool:
            if not isinstance(message.channel, DMChannel) or author != message.author:
                return False
            nonlocal password
            password = message.content
            await message.channel.send(f"The password is: {password}")
            return True

        await ctx.channel.send("DM me your password")
        try:
            await self.bot.wait_for('message', timeout=60.0, check=check)
        except AsyncTimeoutError:
            await ctx.channel.send("Timeout")
            raise PasswordTimeout()
        return password

    @command(name="generate_token", aliases=["gt"])
    @has_permissions(manage_guild=True)
    async def generate_token(
            self,
            ctx,
            permissions: PermissionConverter,
            members: Optional[Greedy[Member]],
            uses: int = 1,
            duration: int = 60.0
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
