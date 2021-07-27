from FieldCreator.Field import Field

from database import Channel


class ChannelGroupField(Field):
    """A field created from a ChannelGroup"""

    def __init__(self, channel: Channel, inline=True):
        self.channel = channel
        self._inline = inline

    @property
    def title(self) -> str:
        return self.channel.name

    @property
    def description(self) -> str:
        return self.channel.id

    @property
    def inline(self) -> bool:
        return self._inline
