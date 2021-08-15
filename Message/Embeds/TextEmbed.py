from abc import ABC

from .NoneEmbed import NoneEmbed
from .BaseLanguageEmbed import BaseLanguageEmbed
from .AuthorColourEmbed import AuthorColourEmbed
from .NowEmbed import NowEmbed


class TextEmbedPartial(BaseLanguageEmbed, AuthorColourEmbed, NowEmbed, ABC):
    """
    An embed that has a title, desc, and author.
    Meant to be extended.
    """


class TextEmbed(TextEmbedPartial, NoneEmbed):
    """
    An embed that has a title, desc, and author.
    Not meant to be extended.
    """
