from abc import ABC, abstractmethod
from typing import Optional, List

from discord import Client, Embed, File
from database import Channel


class Message(ABC):
    """An interface for a message"""

    @property
    @abstractmethod
    def content(self) -> Optional[str]:
        """The text of the message, None if to be skipped"""

    @property
    @abstractmethod
    def embed(self) -> Optional[Embed]:
        """The embed of the message, None if to be skipped"""

    @property
    @abstractmethod
    def attachments(self) -> Optional[List[File]]:
        """The attachments of the message, None if to be skipped"""

    def file(self) -> Optional[File]:
        if self.attachments is None or len(self.attachments) != 1:
            return None
        return self.attachments[0]

    def files(self) -> Optional[List[File]]:
        if self.attachments is None or len(self.attachments) == 1:
            return None
        return self.attachments

    async def post_message(self, client: Client, channel: Channel):
        """Posts a message to a channel"""

        # Return control back, mainly used for wrapping the function with more functionality
        yield client, channel

        kwargs = {
            "content": self.content,
            "embed": self.embed,
            "file": self.file,
            "files": self.files
        }

        for kwarg in kwargs.keys():
            if kwargs[kwarg] is None:
                del kwargs[kwarg]

        client.get_channel(channel.id).send(**kwargs)
