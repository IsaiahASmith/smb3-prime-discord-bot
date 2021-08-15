from abc import ABC
from typing import Optional

from Message.Embeds.Embed import Embed


class ThumbnailEmbed(Embed, ABC):
    """An embed with an Author"""

    def __init__(self, thumbnail_url: str, *args, **kwargs):
        self._thumbnail_url = thumbnail_url
        super().__init__(*args, **kwargs)

    @property
    def thumbnail(self) -> Optional[str]:
        """Returns the url to the thumbnail for the embed, None will be returned for an embed without a thumbnail"""
        return self._thumbnail_url
