# pip install google_trans==3.1.0a0 => this is the correct install for some weird ass reason.
from typing import Optional
from enum import Enum

from discord.ext.commands import Cog, command

import translators as ts

from database import session, Channel


class Language(Enum):
    english = "en"
    spanish = "es"


language_codes = {
    "en": Language.english,
    "english": Language.english,
    "es": Language.spanish,
    "spanish": Language.spanish
}


def translate(message: str, language: Language):
    lan_code = language.value
    return ts.google(message, to_language=lan_code)


class Translate(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="set_channel_language")
    async def set_channel_language(self, ctx, channel_id: Optional[int], language_code: str):
        channel_id = channel_id or ctx.id

        channel = session.query(Channel).filter(Channel.id == channel_id).first()
        if channel is None:
            """The channel has not been initialized, so create it"""
            session.add(Channel(id=channel_id, guild_id=ctx.guild.id))
            channel = session.query(Channel).filter(Channel.id == channel_id).first()

        channel.language = language_codes[language_code]
        session.commit()

        discord_channel = self.bot.get_channel(channel.id)

        await ctx.send(f"Updated channel {discord_channel.name} to have language {channel.language}")

    @command(name="translate")
    async def translate(self, ctx, *, message: str):
        language_code, message = message.split(' ', 1)
        await ctx.send(translate(message, language_codes[language_code]))

    @Cog.listener()
    async def on_ready(self):
        pass

def setup(bot):
    bot.add_cog(Translate(bot))