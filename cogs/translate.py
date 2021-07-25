from typing import Optional
from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog, command

import translators as ts

from database import session

from converters.ChannelConverter import ChannelConverter
from converters.LanguageConverter import LanguageConverter

from Language import Language


def translate(message: str, language: Language):
    return ts.google(message, to_language=language.value)


class Translate(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="set_channel_language", aliases=["scl"])
    async def set_channel_language(
            self,
            ctx,
            channel: ChannelConverter,
            language: LanguageConverter
    ):
        channel.language = language
        session.commit()

        discord_channel = self.bot.get_channel(channel.id)
        embed = Embed(
            title=f"Updated Channel {discord_channel.name}",
            description=f"Changed {discord_channel.name} language to {channel.language.value}",
            colour=ctx.author.colour,
            timestamp=datetime.utcnow()
        )

        await ctx.send(embed=embed)

    @command(name="translate")
    async def translate(self, ctx, language: LanguageConverter, *, message: str):
        embed = Embed(
            colour=ctx.author.colour, description=translate(message, language), timestamp=datetime.utcnow()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Translate(bot))