from typing import List, Set, Optional
from asyncio import sleep
from asyncio import TimeoutError as AsyncTimeoutError
from datetime import datetime

from discord import Embed, Colour, TextChannel, Member, DMChannel
from discord.ext.commands import Cog, command, has_permissions, Greedy

from converters.ChannelConverter import ChannelConverter
from converters.ChannelGroupConverter import ChannelGroupConverter
from database import session, Channel, ChannelGroup, ChannelGroupChannel

from cogs.security import Security

from Message.MessageCreator import MessageCopyCreator

from ChannelAdapter import ChannelAdapter
from Field import Field

from prefix import prefix


def get_groups_by_guild(guild_id: int):
    """Finds all the groups a guild has"""
    return session.query(ChannelGroup).filter(ChannelGroup.guild_id == guild_id)


def list_groups_to_embed(
        groups: List[ChannelGroup],
        title: str = "Channel Groups",
        colour: Optional[Colour] = None
) -> Embed:
    colour = colour or Colour.default()
    embed = Embed(
        title=title,
        colour=colour,
        timestamp=datetime.utcnow()
    )

    fields = [Field(group.name, group.id, False) for group in groups]
    for field in fields:
        field.add_to_embed(embed)

    return embed


def get_group_channels(group: ChannelGroup) -> Set[Channel]:
    """Finds every channel a group contains"""
    return {
        channel for channel in 
        session.query(Channel).join(ChannelGroupChannel).filter(
            ChannelGroupChannel.channel_group_id == group.id
        )
    }


def group_to_embed(
        bot,
        group: ChannelGroup,
        title: str = "Channel Group",
        colour: Optional[Colour] = None
) -> Embed:
    """Provides an embed for a group"""
    colour = colour or Colour.default()
    embed = Embed(
        title=title,
        colour=colour,
        timestamp=datetime.utcnow()
    )

    channels = get_group_channels(group)

    fields = [
        Field(f"Group: {group.name}", f"ID: {group.id}", False),
        *[
            Field(bot.get_channel(channel.id).name, channel.id, True) 
            for channel in channels
        ]
    ]

    for field in fields:
        field.add_to_embed(embed)

    return embed


def get_groups_from_channel(channel: TextChannel) -> Set[ChannelGroup]:
    """Finds every group a channel is associated with"""
    return {
        group for group in
        session.query(ChannelGroup).join(ChannelGroupChannel).join(Channel).filter(
            channel.id == ChannelGroupChannel.channel_id
        )
    }


class ChannelManager(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="channel_groups", aliases=["cg"])
    @has_permissions(manage_guild=True)
    async def channel_groups(self, ctx):
        groups = get_groups_by_guild(ctx.guild.id)
        embed = list_groups_to_embed(groups, colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @command(name="register_channel_group", aliases=["rcg"])
    @has_permissions(manage_guild=True)
    async def register_channel_group(self, ctx, channel_name):
        group = ChannelGroup(guild_id=ctx.guild.id, name=channel_name)
        session.add(group)
        session.commit()
        embed = group_to_embed(self.bot, group, "Registered Channel Group", ctx.author.colour)
        await ctx.send(embed=embed)

    @command(name="remove_channel_group", aliases=["rem_cg"])
    @has_permissions(manage_guild=True)
    async def remove_channel_group(self, ctx, group: ChannelGroupConverter):
        embed = group_to_embed(self.bot, group, "Removed Channel Group", ctx.author.colour)
        session.delete(group)
        session.commit()
        await ctx.send(embed=embed)

    @command(name="register_channel_from_token", aliases=["rcft"])
    @has_permissions(manage_guild=True)
    async def register_channel_from_token(self, ctx, channel: ChannelConverter, group_token: int, password: str):
        security_cog: Security = self.bot.cogs_lookup["security"]
        info = await security_cog.get_hole_info(group_token, ctx.author, password)
        if info is None:
            await ctx.send("Permission Denied")
            return
        group = info[0]
        await security_cog.close_hole(group_token)  # Close the hole as it is useless now
        session.add(ChannelGroupChannel(channel_group_id=group.id, channel_id=channel.id))
        session.commit()
        embed = group_to_embed(self.bot, group, "Channels Registered", ctx.author.colour)
        await ctx.send(embed=embed)

    @command(name="generate_access_token", aliases=["gat"])
    @has_permissions(manage_guild=True)
    async def generate_access_token(
            self,
            ctx,
            group: ChannelGroupConverter,
            members: Greedy[Member],
            duration: Optional[int] = 60.0
    ):
        members = {member for member in members}

        token = None
        dm_channel = None

        def check(message) -> bool:
            if isinstance(message.channel, DMChannel):
                nonlocal token
                nonlocal dm_channel
                token = message.content
                dm_channel = message.channel
                return True
            return False

        try:
            await ctx.channel.send("DM me your password")
            await self.bot.wait_for('message', timeout=60.0, check=check)
        except AsyncTimeoutError:
            await ctx.channel.send("Timeout")
            return None

        await dm_channel.send(f"The password is: {token}")
        security_cog: Security = self.bot.cogs_lookup["security"]
        hole_id = await security_cog.open_hole(members, token, group)
        await ctx.send(f"The group token is {hole_id!s}")

        await sleep(duration)
        await security_cog.close_hole(hole_id)

    @command(name="register_channel", aliases=["rc"])
    @has_permissions(manage_guild=True)
    async def register_channel(self, ctx, channel: ChannelConverter, group: ChannelGroupConverter):
        session.add(ChannelGroupChannel(channel_group_id=group.id, channel_id=channel.id))
        session.commit()
        embed = group_to_embed(self.bot, group, "Channels Registered", ctx.author.colour)
        await ctx.send(embed=embed)

    @command(name="unregister_channel", aliases=["urc"])
    @has_permissions(manage_guild=True)
    async def unregister_channel(self, ctx, channel: ChannelConverter, group: ChannelGroupConverter):
        channel_group_channel = (
            session.query(ChannelGroupChannel)
                .filter(
                (ChannelGroupChannel.channel_group_id == group.id) & (ChannelGroupChannel.channel_id == channel.id))
                .first()
        )
        session.delete(channel_group_channel)
        session.commit()
        embed = group_to_embed(self.bot, group, "Channels Registered", ctx.author.colour)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_conversation(self, message):
        sender_cog = self.bot.cogs_lookup["sender"]

        await sender_cog.send_once(
            ChannelAdapter.from_discord_channel(message.channel).groups,
            MessageCopyCreator(message),
            {message.channel.id}
        )


def setup(bot):
    cog = ChannelManager(bot)
    bot.add_cog(cog)
    return cog
