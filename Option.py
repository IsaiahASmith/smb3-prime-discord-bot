from dataclasses import dataclass
from typing import List, Set
from datetime import datetime

from discord import Embed
from discord import Colour, Member

from Field import Field
from Response import Response


@dataclass
class Option:
    """A series of responses to choose from"""

    question: str
    description: str
    colour: Colour
    responses: List[Response]
    responders: Set[Member]

    def to_embed(self) -> Embed:
        """Creates an embed from itself"""
        embed = Embed(
            title=self.question, description=self.description, colour=self.colour, timestamp=datetime.utcnow()
        )

        fields = [Field(response.name, response.description, False) for response in self.responses]
        for field in fields:
            field.add_to_embed(embed)

        return embed
