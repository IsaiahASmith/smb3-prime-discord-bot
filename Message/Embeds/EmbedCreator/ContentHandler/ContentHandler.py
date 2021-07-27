from abc import ABC, abstractmethod

from Message.Embeds.EmbedCreator.MetaMessage import MetaMessage


class ContentHandler(ABC):
    """Takes the content from a message and divides it into the title and description"""

    def __init__(self, meta: MetaMessage):
        self.meta = meta

    @property
    @abstractmethod
    def title(self) -> str:
        """Returns the title of the embed"""

    @property
    @abstractmethod
    def description(self) -> str:
        """Returns the description of the embed"""
