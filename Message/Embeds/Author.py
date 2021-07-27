from dataclasses import dataclass
from typing import Union

from discord import Colour


@dataclass
class Author:
    name: str
    url: str
    icon_url: str
    colour: Union[int, Colour]