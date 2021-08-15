from typing import Union, Optional, List

from discord import Attachment

from .TextEmbed import TextEmbed
from .ImageTextEmbed import ImageTextEmbed
from .ThumbnailTextEmbed import ThumbnailTextEmbed


image_types = ["png", "jpeg", "gif", "jpg"]


def has_an_image(attachments: List[Attachment], index: int = 0) -> bool:
    """Determines if there is an embed inside any attachment"""
    return any(attachments[index].filename.lower().endswith(image) for image in image_types)


def get_embed_from_message(
    title: Optional[str] = None, attachments: Optional[List[Attachment]] = None, **kwargs
) -> Union[TextEmbed, ImageTextEmbed, ThumbnailTextEmbed]:
    """Creates an embed for something a Member said"""
    if attachments is None or not len(attachments) or not has_an_image(attachments):
        return TextEmbed(title=title, attachments=attachments, **kwargs)
    elif title:
        return ImageTextEmbed.from_attachments(title=title, attachments=attachments, **kwargs)
    else:
        return ThumbnailTextEmbed.from_attachments(title=title, attachments=attachments, **kwargs)
