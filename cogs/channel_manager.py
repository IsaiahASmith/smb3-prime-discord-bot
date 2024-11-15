from typing import List, Optional
from datetime import datetime

from discord import Embed, Colour, TextChannel
from discord.ext.commands import Cog, command, has_permissions

from converters.ChannelConverter import ChannelConverter
from converters.ChannelGroupConverter import ChannelGroupConverter
from database import session, ChannelGroup, ChannelGroupChannel, Guild


from Message.MessageCreator import MessageCopyCreator

from ChannelAdapter import ChannelAdapter
from Field import Field

from prefix import prefix


def list_groups_to_embed(
    groups: List[ChannelGroup], title: str = "Channel Groups", colour: Optional[Colour] = None
) -> Embed:
    colour = colour or Colour.default()
    embed = Embed(title=title, colour=colour, timestamp=datetime.utcnow())

    fields = [Field(group.name, group.id, False) for group in groups]
    for field in fields:
        field.add_to_embed(embed)

    return embed


def group_to_embed(bot, group: ChannelGroup, title: str = "Channel Group", colour: Optional[Colour] = None) -> Embed:
    """Provides an embed for a group"""
    colour = colour or Colour.default()
    embed = Embed(title=title, colour=colour, timestamp=datetime.utcnow())

    fields = [
        Field(f"Group: {group.name}", f"ID: {group.id}", False),
        *[Field(bot.get_channel(channel.id).name, channel.id, True) for channel in group.channels],
    ]

    for field in fields:
        field.add_to_embed(embed)

    return embed


class ChannelManager(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="channel_groups", aliases=["cg"])
    @has_permissions(manage_guild=True)
    async def channel_groups(self, ctx):
        embed = list_groups_to_embed(Guild.query.get(ctx.guild.id).channel_groups, colour=ctx.author.colour)
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
        group.channels.remove(channel)
        session.commit()
        embed = group_to_embed(self.bot, group, "Channels Registered", ctx.author.colour)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_message(self, message):
        sender_cog = self.bot.cogs_lookup["sender"]

        if message.author.bot or message.content.startswith(prefix(message.guild)):
            return

        if not isinstance(message.channel, TextChannel):
            return

        channel = ChannelAdapter.from_discord_channel(message.channel)
        if channel.channel is None:
            return
        groups = channel.channel.groups
        if groups is None:
            return

        await sender_cog.send_once(
            groups,
            MessageCopyCreator(message),
            {message.channel.id},
        )


def setup(bot):
    cog = ChannelManager(bot)
    bot.add_cog(cog)
    return cog
