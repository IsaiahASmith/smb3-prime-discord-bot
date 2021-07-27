from typing import Type

from discord import Client, Message
from discord import Embed as DiscordEmbed

from database import Channel

from Message.Embeds.Embed import Embed
from Message.Embeds.EmbedCreator.MetaMessage import MetaMessage
from Message.Embeds.EmbedHandler.EmbedHandler import EmbedHandler
from Message.Embeds.EmbedCreator.ContentHandler.ContentHandler import ContentHandler


class EmbedCreator:
    """Creates an embed from an embed creator"""

    def __init__(self, message: Message, embed: Type[Embed], content_handler: Type[ContentHandler]):
        self.message = message
        self.embed = embed
        self.content_handler = content_handler
        self.client = None
        self.channel = None

    def set_client_and_channel(self, client: Client, channel: Channel):
        """We must set the client and channel after the fact, as it is only know at send"""
        self.client = client
        self.channel = channel

    @property
    def meta(self) -> MetaMessage:
        return MetaMessage(self.message, self.client, self.channel)

    async def create_embed(self) -> DiscordEmbed:
        """Creates the embed for the message"""
        return await EmbedHandler(self.embed, self.content_handler, self.meta).create_embed()
