from abc import ABC, abstractmethod
from typing import Union, Optional, List
from datetime import datetime

from discord import Colour
from discord import Embed as DiscordEmbed

from cogs.translate import translate

from FieldCreator.Field import Field

from Language import Language

from Message.Embeds.Author import Author
from Message.Embeds.Footer import Footer


class Embed(ABC):
    """A interface to create an Embed"""
    def __init__(self, *args, **kwargs):
        """Accepts multiple arguments to help with inheritance"""

    @property
    @abstractmethod
    def author(self) -> Optional[Author]:
        """Returns the author of the embed, None will be returned for an embed without an author"""

    @property
    @abstractmethod
    def colour(self) -> Optional[Union[Colour, int]]:
        """Returns the colour of the embed, None will be returned if default is desired"""

    @property
    @abstractmethod
    def description(self) -> Optional[str]:
        """Returns the description of the embed, None will be returned for an embed without a description"""

    @property
    @abstractmethod
    def fields(self) -> Optional[List[Field]]:
        """Returns the fields of the embed, None will be returned if there are no fields"""

    @property
    @abstractmethod
    def footer(self) -> Optional[Footer]:
        """Returns the footer of the embed, None will be returned for an embed without a footer"""

    @property
    @abstractmethod
    def image(self) -> Optional[str]:
        """Returns the url to the image for the embed, None will be returned for an embed without an image"""

    @property
    @abstractmethod
    def thumbnail(self) -> Optional[str]:
        """Returns the url to the thumbnail for the embed, None will be returned for an embed without a thumbnail"""

    @property
    @abstractmethod
    def timestamp(self) -> Optional[datetime]:
        """Returns the timestamp for the embed, None will be returned for an embed without a timestamp"""

    @property
    @abstractmethod
    def title(self) -> Optional[str]:
        """Returns the title for the embed, None will be returned for an embed without a title"""

    @property
    @abstractmethod
    def language(self) -> Optional[Language]:
        """Returns the language the embed should be returned in, None will be returned for no preference"""

    @property
    @abstractmethod
    def current_language(self) -> Optional[Language]:
        """Returns the language of the incoming text"""

    async def create_embed(self) -> DiscordEmbed:
        """Creates a discord embed"""

        kwargs = {
            "title": translate(self.title, self.language, self.current_language),
            "description": translate(self.description, self.language, self.current_language),
            "colour": self.colour,
            "timestamp": self.timestamp
        }

        kwargs_to_del = []
        for kwarg in kwargs.keys():
            if kwargs[kwarg] is None:
                kwargs_to_del.append(kwarg)

        for kwarg in kwargs_to_del:
            del kwargs[kwarg]

        embed = DiscordEmbed(**kwargs)

        if self.author is not None:
            kwargs = {"name": self.author.name, "url": self.author.url, "icon_url": self.author.icon_url}
            embed.set_author(**kwargs)

        if self.footer is not None:
            kwargs = {
                "text": translate(self.footer.text, self.language, self.current_language),
                "icon_url": self.footer.icon_url
            }
            embed.set_footer(**kwargs)

        if self.image is not None:
            embed.set_image(url=self.image)

        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail)

        if self.fields is not None:
            for field in self.fields:
                field.add_field(self)

        return embed
