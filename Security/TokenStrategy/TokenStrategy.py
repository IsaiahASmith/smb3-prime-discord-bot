from typing import Optional, Set
from abc import ABC, abstractmethod

from discord import Member, TextChannel, Guild

from Security.Permission.Permission import Permission
from Security.SecureMemberAdapter import SecureMemberAdapter
from Security.Token import Token


class TokenStrategy(ABC):
    """A series of commands to be used to generate tokens"""

    @abstractmethod
    async def generate_token(
            self,
            author: SecureMemberAdapter,
            permissions: Permission,
            members: Optional[Set[Member]],
            uses: int = 1,
            duration: int = 60.0
    ):
        """Generates a token to be used by users"""

    @abstractmethod
    async def get_token_permissions(
            self,
            token: Token,
            member: Member,
            channel: TextChannel,
            guild: Guild
    ) -> Permission:
        """Retrieves the permissions of the token"""

    @abstractmethod
    async def use_token(
            self,
            token: Token,
            member: Member,
            channel: TextChannel,
            guild: Guild
    ):
        """Expends a token"""
