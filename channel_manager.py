from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog, command, has_permissions

from database import session, Channel, ChannelGroup, ChannelGroupChannel


class ChannelManager(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="register_channel_group", aliases=["rcg"])
    @has_permissions(manage_guild=True)
    async def register_channel_group(self, ctx, channel_name):
        session.add(ChannelGroup(guild_id=ctx.guild.id, name=channel_name))
        session.commit()

    @command(name="remove_channel_group", aliases=["rem_cg"])
    @has_permissions(manage_guild=True)
    async def remove_channel_group(self, ctx, group_id: int):
        group = session.query(ChannelGroup).filter(ChannelGroup.id == group_id).first()
        session.delete(group)
        session.commit()

    @command(name="register_channel", aliases=["rc"])
    @has_permissions(manage_guild=True)
    async def register_channel(self, ctx, channel_id, group_id):
        channel_ids = {channel.id for channel in ctx.guild.channels}
        if channel_id not in channel_ids:
            """The channel id was not found"""
            await ctx.send(f"Channel {channel_id} was not found")
            return

        group = session.query(ChannelGroup).filter(ChannelGroup.id == group_id).first()
        if group.guild_id != ctx.guild.id or group is None:
            """Either we specified a forbidden group ID or the group does not exist"""
            await ctx.send(f"Group {group_id} was not found.")
            return

        channel = session.query(Channel).filter(Channel.id == channel_id).first()
        if channel is None:
            """The channel has not been initialized, so create it"""
            session.add(Channel(id=channel_id, guild_id=ctx.guild.id))

        session.add(ChannelGroupChannel(channel_group_id=group.id, channel_id=channel.id))
        session.commit()

    @command(name="unregister_channel", aliases=["urc"])
    @has_permissions(manage_guild=True)
    async def unregister_channel(self, ctx, channel_id, group_id):
        channel_ids = {channel.id for channel in ctx.guild.channels}
        if channel_id not in channel_ids:
            """The channel id was not found"""
            await ctx.send(f"Channel {channel_id} was not found")
            return

        group = session.query(ChannelGroup).filter(ChannelGroup.id == group_id).first()
        if group.guild_id != ctx.guild.id or group is None:
            """Either we specified a forbidden group ID or the group does not exist"""
            await ctx.send(f"Group {group_id} was not found.")
            return

        channel = session.query(Channel).filter(Channel.id == channel_id).first()
        if channel is None:
            """The channel has not been initialized, so do not do anything"""
            return

        channel_group_channel = session.query(ChannelGroupChannel).filter(
            (ChannelGroupChannel.channel_group_id == group.id) & (ChannelGroupChannel.channel_id == channel.id)
        ).first()
        session.delete(channel_group_channel)
        session.commit()

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            channel = session.query(Channel).filter(Channel.id == message.channel.id).first()

            if channel is not None:
                channel_groups = session.query(ChannelGroup).join(ChannelGroupChannel).join(Channel).filter(
                    channel.id == ChannelGroupChannel.channel_id
                )

                print("channel groups", channel_groups)

                embed = Embed(
                    colour=message.author.colour,
                    description=message.content,
                    timestamp=datetime.utcnow()
                )

                embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)

                sent_channels = {channel.id}
                for channel_group in channel_groups:
                    for channel in channel_group.channels:
                        if channel.id not in sent_channels:
                            await channel.send(embed=embed)
                            sent_channels.add(channel.id)

    @Cog.listener()
    async def on_ready(self):
        pass


def setup(bot):
    bot.add_cog(ChannelManager(bot))
