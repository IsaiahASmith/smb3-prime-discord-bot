from abc import ABC
from typing import Optional
from Language import Language

from Message.Embeds.Embed import Embed


class LanguageEmbed(Embed, ABC):
    """An embed with language set"""

    def __init__(self, language: Optional[Language], current_language: Optional[Language], *args, **kwargs):
        self._language = language
        self._current_language = current_language
        super().__init__(*args, **kwargs)

    @property
    def language(self) -> Optional[Language]:
        """Returns the language the embed should be returned in, None will be returned for no preference"""
        return self._language

    @property
    def current_language(self) -> Optional[Language]:
        """Returns the language of the incoming text"""
        return self._current_language
