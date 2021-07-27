from typing import Optional
from abc import ABC

from .BaseEmbed import BaseEmbed
from .LanguageEmbed import LanguageEmbed

from cogs.translate import translate


class BaseLanguageEmbed(LanguageEmbed, BaseEmbed, ABC):
    """An embed with both a description and title that are automatically translated"""

    @property
    def description(self) -> Optional[str]:
        """Returns the description of the embed, None will be returned for an embed without a description"""
        return translate(self._description, language=self.language, from_language=self.current_language)

    @property
    def title(self) -> Optional[str]:
        """Returns the title for the embed, None will be returned for an embed without a title"""
        return translate(self._title, language=self.language, from_language=self.current_language)
