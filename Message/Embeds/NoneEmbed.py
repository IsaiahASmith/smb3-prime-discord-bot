from typing import Union, Optional, List
from datetime import datetime

from discord import Colour
from FieldCreator.Field import Field

from Language import Language

from Message.Embeds.Embed import Embed
from Message.Embeds.Author import Author
from Message.Embeds.Footer import Footer


class NoneEmbed(Embed):
    """An embed without anything"""

    @property
    def author(self) -> Optional[Author]:
        """Returns the author of the embed, None will be returned for an embed without an author"""
        return None

    @property
    def colour(self) -> Optional[Union[Colour, int]]:
        """Returns the colour of the embed, None will be returned if default is desired"""
        return None

    @property
    def description(self) -> Optional[str]:
        """Returns the description of the embed, None will be returned for an embed without a description"""
        return None

    @property
    def fields(self) -> Optional[List[Field]]:
        """Returns the fields of the embed, None will be returned if there are no fields"""
        return None

    @property
    def footer(self) -> Optional[Footer]:
        """Returns the footer of the embed, None will be returned for an embed without a footer"""
        return None

    @property
    def image(self) -> Optional[str]:
        """Returns the url to the image for the embed, None will be returned for an embed without an image"""
        return None

    @property
    def thumbnail(self) -> Optional[str]:
        """Returns the url to the thumbnail for the embed, None will be returned for an embed without a thumbnail"""
        return None

    @property
    def timestamp(self) -> Optional[datetime]:
        """Returns the timestamp for the embed, None will be returned for an embed without a timestamp"""
        return None

    @property
    def title(self) -> Optional[str]:
        """Returns the title for the embed, None will be returned for an embed without a title"""
        return None

    @property
    def language(self) -> Optional[Language]:
        """Returns the language the embed should be returned in, None will be returned for no preference"""
        return None

    @property
    def current_language(self) -> Optional[Language]:
        """Returns the language of the incoming text"""
        return None
