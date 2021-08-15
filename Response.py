from dataclasses import dataclass

from discord import Emoji


@dataclass
class Response:
    """A response to a question"""

    name: str
    description: str
    emoji: Emoji
