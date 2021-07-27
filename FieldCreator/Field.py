from abc import ABC, abstractmethod

from discord import Embed


class Field(ABC):
    """The interface to create a field"""

    @property
    @abstractmethod
    def title(self) -> str:
        """The title of the field"""

    @property
    @abstractmethod
    def description(self) -> str:
        """The description of the field"""

    @property
    @abstractmethod
    def inline(self) -> bool:
        """If the field sits inline or alone"""

    def add_field(self, embed: Embed):
        """Adds a field to the provided embed"""
        embed.add_field(name=self.title, value=self.description, inline=self.inline)
