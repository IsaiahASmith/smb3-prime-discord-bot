from abc import ABC
from typing import Optional

from Message.Embeds.Embed import Embed


class ImageEmbed(Embed, ABC):
    """An embed with an Author"""

    def __init__(self, image_url: str, *args, **kwargs):
        self._image_url = image_url
        super().__init__(*args, **kwargs)

    @property
    def image(self) -> Optional[str]:
        """Returns the url to the image for the embed, None will be returned for an embed without an image"""
        return self._image_url
