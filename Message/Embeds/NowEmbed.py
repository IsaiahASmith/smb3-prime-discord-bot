from abc import ABC
from typing import Optional
from datetime import datetime

from Message.Embeds.Embed import Embed


class NowEmbed(Embed, ABC):
    """An embed that sets the timestamp as utfnow()"""
    @property
    def timestamp(self) -> Optional[datetime]:
        """Returns the timestamp for the embed, None will be returned for an embed without a timestamp"""
        return datetime.utcnow()
