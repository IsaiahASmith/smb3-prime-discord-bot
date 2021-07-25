from typing import Optional, List

from discord.ext.commands import Converter, CommandError

from Language import Language


_language_codes = {
    "en": Language.english,
    "english": Language.english,
    "es": Language.spanish,
    "spanish": Language.spanish,
    "pt-BR": Language.portuguese_brazil,
    "brazil": Language.portuguese_brazil,
    "de": Language.german,
    "german": Language.german,
    "it": Language.italian,
    "italian": Language.italian
}


def get_language(name: str) -> Optional[Language]:
    name = name.lower()
    if name in _language_codes:
        return _language_codes[name]


class LanguageConverter(Converter):
    """Tries and finds a valid ChannelGroup"""
    async def convert(self, ctx, argument) -> Optional[Language]:
        return get_language(argument)
