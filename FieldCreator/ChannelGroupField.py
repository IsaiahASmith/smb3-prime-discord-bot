from FieldCreator.Field import Field

from database import ChannelGroup


class ChannelGroupField(Field):
    """A field created from a ChannelGroup"""

    def __init__(self, group: ChannelGroup, inline=True):
        self.group = group
        self._inline = inline

    @property
    def title(self) -> str:
        return self.group.name

    @property
    def description(self) -> str:
        return self.group.id

    @property
    def inline(self) -> bool:
        return self._inline
