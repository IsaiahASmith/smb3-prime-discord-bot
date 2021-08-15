from typing import Type, Optional, List
from discord import Embed as DiscordEmbed

from discord import Message, Client, Attachment

from database import Channel

from ChannelAdapter import ChannelAdapter
from Language import Language

from Message.Embeds.Embed import Embed
from Message.Embeds.Author import Author

from Message.Embeds.EmbedCreator.ContentHandler.ContentHandler import ContentHandler

from Message.Embeds.EmbedCreator.MetaMessage import MetaMessage


class EmbedHandler:
    """Decomposes a message, client, and channel into the components of an embed"""

    def __init__(self, embed: Type[Embed], content_handler: Type[ContentHandler], meta: MetaMessage):
        self.embed = embed
        self.content_handler = content_handler(meta=meta)
        self.meta = meta

    @property
    def message(self) -> Message:
        return self.meta.message

    @property
    def client(self) -> Optional[Client]:
        return self.meta.client

    @property
    def channel(self) -> Optional[Channel]:
        return self.meta.channel

    @property
    def title(self) -> Optional[str]:
        return self.content_handler.title

    @property
    def description(self) -> Optional[str]:
        return self.content_handler.description

    @property
    def language(self) -> Optional[Language]:
        return self.meta.channel.language

    @property
    def current_language(self) -> Optional[Language]:
        return ChannelAdapter.from_discord_channel(self.meta.message.channel).language

    @property
    def attachments(self) -> Optional[List[Attachment]]:
        return self.meta.message.attachments

    @property
    def author(self) -> Author:
        return Author(
            name=self.message.author.name,
            colour=self.message.author.colour,
            url=self.message.author.avatar_url,
            icon_url=self.message.author.avatar_url,
        )

    async def create_embed(self) -> DiscordEmbed:
        embed = self.embed(
            title=self.title,
            description=self.description,
            language=self.language,
            current_language=self.current_language,
            author=self.author,
            attachments=self.attachments,
        )

        return await embed.create_embed()
