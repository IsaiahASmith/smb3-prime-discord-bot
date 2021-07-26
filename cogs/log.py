from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog


_channel_id = 868088666134822922


class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_user_update(self, before, after):
        """A member changed their part of the profile"""

        if before.discriminator != after.discriminator:
            embed = Embed(
                title="Discriminator Change",
                colour=after.colour,
                timestamp=datetime.utcnow()
            )

            fields = [
                ("Before", before.discriminator, False),
                ("After", after.discriminator, False)
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_thumbnail(url=after.avatar_url)

            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)

            await self.bot.get_channel(_channel_id).send(embed=embed)

        if before.avatar_url != after.avatar_url:
            embed = Embed(
                title="Avatar Change",
                colour=after.colour,
                timestamp=datetime.utcnow()
            )

            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)

            await self.bot.get_channel(_channel_id).send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        """A member changed their nickname"""

        if before.display_name != after.display_name:
            embed = Embed(
                title="Nickname Change",
                colour=after.colour,
                timestamp=datetime.utcnow()
            )

            fields = [
                ("Before", before.display_name, False),
                ("After", after.display_name, False)
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_thumbnail(url=after.avatar_url)
            await self.bot.get_channel(_channel_id).send(embed=embed)

        if before.roles != after.roles:
            embed = Embed(
                title="Roles Change",
                colour=after.colour,
                timestamp=datetime.utcnow()
            )

            fields = [
                ("Before", ", ".join([r.mention for r in before.roles]), False),
                ("After", ", ".join([r.mention for r in after.roles]), False)
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_thumbnail(url=after.avatar_url)
            await self.bot.get_channel(_channel_id).send(embed=embed)


    @Cog.listener()
    async def on_message_edit(self, before, after):
       if not after.author.bot:
            if before.content != after.content:
                embed = Embed(
                    title="Message Edit",
                    description=f"Edit by {after.author.display_name}",
                    colour=after.author.colour,
                    timestamp=datetime.utcnow()
                )

                fields = [
                    ("Before", before.content, False),
                    ("After", after.content, False)
                ]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                embed.set_thumbnail(url=after.author.avatar_url)
                await self.bot.get_channel(_channel_id).send(embed=embed)


    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = Embed(
                title="Message Deletion",
                description=f"Action by {message.author.display_name}",
                colour=message.author.colour,
                timestamp=datetime.utcnow()
            )

            fields = [
                ("Delete", message.content, False)
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_thumbnail(url=message.author.avatar_url)
            await self.bot.get_channel(_channel_id).send(embed=embed)


def setup(bot):
    cog = Log(bot)
    bot.add_cog(cog)
    return cog