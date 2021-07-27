from abc import ABC
from typing import List

from discord import Attachment

from .NoneEmbed import NoneEmbed
from .TextEmbed import TextEmbedPartial as TextEmbed
from .ThumbnailEmbed import ThumbnailEmbed


class ThumbnailTextEmbedPartial(ThumbnailEmbed, TextEmbed, ABC):
    """
    An embed that has a title, desc, thumbnail, and author.
    Meant to be extended.
    """

    @classmethod
    def from_attachments(cls, attachments: List[Attachment], **kwargs):
        return cls(**kwargs, thumbnail_url=attachments[0].url)


class ThumbnailTextEmbed(ThumbnailTextEmbedPartial, NoneEmbed):
    """
    An embed that has a title, desc, thumbnail, and author.
    Not meant to be extended.
    """