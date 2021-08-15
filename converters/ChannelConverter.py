from discord.ext.commands import TextChannelConverter

from database import session, Channel


class ChannelConverter(TextChannelConverter):
    """An advanced TextChannelConverter, to automatically register channels the database"""

    async def convert(self, ctx, argument):
        channel = await super().convert(ctx, argument)
        sql_channel = session.query(Channel).filter(Channel.id == channel.id).first()
        if sql_channel is None:
            """The channel has not been initialized, so create it"""
            sql_channel = Channel(id=channel.id, name=channel.name, guild_id=ctx.guild.id)
            session.add(sql_channel)
            session.commit()
        return sql_channel
