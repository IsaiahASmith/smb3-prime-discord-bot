from dataclasses import dataclass
from typing import Optional

from discord import Client, Message

from database import Channel


@dataclass
class MetaMessage:
    message: Message
    client: Optional[Client]
    channel: Optional[Channel]
