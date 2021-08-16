from typing import Optional, List
from asyncio import TimeoutError as AsyncTimeoutError

from discord import Member, Message, TextChannel
from discord.ext.commands import Cog, command, has_permissions, Greedy, Context

from converters.PermissionConverter import PermissionChannelConverter

from Security.MemberAdapter.MemberChannelAdapter import MemberChannelAdapter
from Security.TokenStrategy.BasicTokenStrategy import BasicTokenStrategy
from Security.TokenStrategy.TokenHandlerStrategy.BasicTokenHandlerStrategy import BasicTokenHandlerStrategy


class PasswordTimeout(Exception):
    def __init__(self, message="Failed to create a password before timeout"):
        super().__init__(message)


class Security(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.toke_strategy = BasicTokenStrategy(BasicTokenHandlerStrategy(bot.scheduler))

    async def ask_user_for_password(self, author: Member, channel: TextChannel, password: str = "") -> str:
        """Asks the user for a password"""

        async def password_check(message: Message) -> bool:
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
        return password

    async def generate_token_password(self, ctx: Context) -> str:
        """Asks the member for a password"""
        return await self.ask_user_for_password(ctx.author, ctx.channel)

    @command(name="generate_token", aliases=["gt"])
    @has_permissions(manage_guild=True)
    async def generate_token(
        self,
        ctx: Context,
        permissions: PermissionChannelConverter,
        members: Optional[Greedy[Member]],
        uses: int = 1,
        duration: float = 60.0,
    ):
        members: Optional[List[Member]]
        author = MemberChannelAdapter(ctx.author, ctx.channel)
        if members is not None:
            members = set(members)
        self.token_strategy.generate_token(author, permissions, members, uses, duration)


def setup(bot):
    cog = Security(bot)
    bot.add_cog(cog)
    return cog
