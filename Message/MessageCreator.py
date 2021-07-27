from typing import Optional, List, Tuple

from discord import Client, File, Embed, Attachment
from discord import Message as DiscordMessage

from database import Channel

from Message.Message import Message
from Message.Attachments.NoneAttachment import NoneAttachment

from Message.Embeds.EmbedCreator.EmbedCreator import EmbedCreator
from Message.Embeds.EmbedCreator.ContentHandler.OneSentenceTitleContentHandler import OneSentenceTitleContentHandler
from Message.Embeds.FromMessageEmbed import get_embed_from_message


class MessageCopyCreator(Message):
    """Copies a message"""
    def __init__(self, message: DiscordMessage):
        self.message = message
        self.embed_creator = EmbedCreator(self.message, get_embed_from_message, OneSentenceTitleContentHandler)

    @property
    async def content(self) -> Optional[str]:
        """
        The text of the message, None if to be skipped
        In this case, it just provides the links to the respective files included.
        """
        if self.attachments is None:
            return None
        return "\n".join([attachment.url for attachment in self.attachments])

    @property
    async def embed(self) -> Optional[Embed]:
        """The embed of the message, None if to be skipped"""
        return await self.embed_creator.create_embed()

    @property
    async def files(self) -> Tuple[Optional[File], Optional[List[File]]]:
        """The attachments of the message, None if to be skipped"""
        return await NoneAttachment(self.message).create_attachments()

    @property
    def attachments(self) -> Optional[List[Attachment]]:
        return self.message.attachments

    async def post_message(self, client: Client, channel: Channel):
        """Posts a message to a channel"""

        self.embed_creator.set_client_and_channel(client, channel)

        files = await self.files

        kwargs = {
            "embed": await self.embed,
            "file": files[0],
            "files": files[1]
        }

        kwargs_to_del = []
        for kwarg in kwargs.keys():
            if kwargs[kwarg] is None:
                kwargs_to_del.append(kwarg)

        for kwarg in kwargs_to_del:
            del kwargs[kwarg]

        channel = client.get_channel(channel.id)
        await channel.send(**kwargs)

        content = await self.content
        if content:
            await channel.send(content=content)
