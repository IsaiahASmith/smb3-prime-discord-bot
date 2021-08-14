from typing import Optional, Set
from abc import ABC, abstractmethod

from discord import Member, TextChannel, Guild

from Security.Token import Token


class TokenHandlerStrategy(ABC):
    """Maintains an active list of tokens that are in use"""

    @abstractmethod
    def get_tokens(self, member: Member, guild: Guild, channel: Optional[TextChannel] = None) -> Set[Token]:
        """Provides all valid tokens for a given user"""

    @abstractmethod
    def add_token(self, token: Token, duration: float):
        """Adds a token to be maintained"""

    @abstractmethod
    def del_token(self, token_id: int):
        """Deletes a token to no longer be maintained"""
