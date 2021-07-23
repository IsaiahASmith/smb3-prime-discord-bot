# pip install google_trans==3.1.0a0 => this is the correct install for some weird ass reason.
from enum import Enum

from discord.ext.commands import Cog, command

import translators as ts

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

    @command(name="translate")
    async def translate(self, ctx, *, message: str):
        language_code, message = message.split(' ', 1)
        await ctx.send(translate(message, language_codes[language_code]))

    @Cog.listener()
    async def on_ready(self):
        pass

def setup(bot):
    bot.add_cog(Translate(bot))