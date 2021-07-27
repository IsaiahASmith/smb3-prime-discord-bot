from abc import ABC
from typing import Optional

from Message.Embeds.Embed import Embed


class BaseEmbed(Embed, ABC):
    """An embed with a title and description"""
    def __init__(self, title: str, description: str, *args, **kwargs):
        self._title = title
        self._description = description
        super().__init__(*args, **kwargs)

    @property
    def description(self) -> Optional[str]:
        """Returns the description of the embed, None will be returned for an embed without a description"""
        return self._description

    @property
    def title(self) -> Optional[str]:
        """Returns the title for the embed, None will be returned for an embed without a title"""
        return self._title
