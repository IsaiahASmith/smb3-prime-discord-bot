from abc import ABC
from typing import List

from discord import Attachment

from .NoneEmbed import NoneEmbed
from .TextEmbed import TextEmbedPartial as TextEmbed
from .ImageEmbed import ImageEmbed


class ImageTextEmbedPartial(ImageEmbed, TextEmbed, ABC):
    """
    An embed that has a title, desc, image, and author.
    Meant to be extended.
    """

    @classmethod
    def from_attachments(cls, attachments: List[Attachment], **kwargs):
        return cls(**kwargs, image_url=attachments[0].url)


class ImageTextEmbed(ImageTextEmbedPartial, NoneEmbed):
    """
    An embed that has a title, desc, image, and author.
    Not meant to be extended.
    """
