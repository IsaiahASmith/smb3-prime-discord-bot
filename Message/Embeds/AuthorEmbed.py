from abc import ABC
from typing import Optional

from Message.Embeds.Embed import Embed
from Message.Embeds.Author import Author


class AuthorEmbed(Embed, ABC):
    """An embed with an Author"""

    def __init__(self, author: Author, *args, **kwargs):
        self._author = author
        super().__init__(*args, **kwargs)

    @property
    def author(self) -> Optional[Author]:
        """Returns the author of the embed, None will be returned for an embed without an author"""
        return self._author
