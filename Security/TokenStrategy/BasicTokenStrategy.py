from typing import Optional, Set

from discord import Member, TextChannel, Guild

from Security.Permission.Permission import Permission
from Security.Token import Token
from Security.SecureMemberAdapter import SecureMemberAdapter
from Security import validate

from .TokenHandlerStrategy.TokenHandlerStrategy import TokenHandlerStrategy
from .ForbiddenTokenException import ForbiddenTokenException
from .NonMemberTokenException import NonMemberTokenException
from .TokenStrategy import TokenStrategy


class BasicTokenStrategy(TokenStrategy):
    """A series of commands to be used to generate tokens"""

    def __init__(self, handler: TokenHandlerStrategy):
        self.handler = handler
        super().__init__()

    async def generate_token(
            self,
            author: SecureMemberAdapter,
            permissions: Permission,
            members: Optional[Set[Member]],
            uses: int = 1,
            duration: float = 60.0
    ):
        """Generates a token to be used by users"""
        if not validate(permissions, author.permissions):
            raise ForbiddenTokenException(author.member, permissions, author.permissions)
        if members is None:
            raise NonMemberTokenException(author, permissions, uses, duration)
        self.handler.add_token(Token(permissions, uses, members), duration)

    async def get_token_permissions(
            self,
            token: Token,
            member: Member,
            channel: TextChannel,
            guild: Guild
    ):
        """Retrieves the permissions of the token"""

    async def use_token(
            self,
            token: Token,
            member: Member,
            channel: TextChannel,
            guild: Guild
    ):
        """Expends a token"""
