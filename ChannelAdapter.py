from typing import Optional

from cachetools import cachedmethod

from discord import TextChannel

from database import session, Channel

from Language import Language


class ChannelAdapter:
    """An adapter to exchange between our database Channel and Discord's TextChannel freely"""

    def __init__(self, channel: Channel):
        self.channel = channel

    @classmethod
    def from_discord_channel(cls, channel: TextChannel):
        return cls(session.query(Channel).get(channel.id))

    @property
    def language(self) -> Optional[Language]:
        return self.channel.language
