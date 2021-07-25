from dataclasses import dataclass

from discord import Embed


@dataclass
class Field:
    name: str
    value: str
    inline: bool

    def add_to_embed(self, embed: Embed):
        embed.add_field(name=self.name, value=self.value, inline=self.inline)
