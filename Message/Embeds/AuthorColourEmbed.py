from abc import ABC
from typing import Optional, Union

from discord import Colour

from Message.Embeds.AuthorEmbed import AuthorEmbed


class AuthorColourEmbed(AuthorEmbed, ABC):
    """An embed with an Author colour"""

    @property
    def colour(self) -> Optional[Union[Colour, int]]:
        """Returns the colour of the embed, None will be returned if default is desired"""
        return self.author.colour
