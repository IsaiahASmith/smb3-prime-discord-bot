from typing import Optional, Generator, Dict, Set
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from discord import Member, TextChannel, Guild

from Security.Token import Token
from Security.Permission import Permission

from .TokenHandlerStrategy import TokenHandlerStrategy


def token_id_generator() -> Generator[int]:
    """Generates a new token id each call"""
    token_id = 0
    while True:
        yield token_id
        token_id += 1


class BasicTokenHandlerStrategy(TokenHandlerStrategy):
    """Maintains an active list of tokens that are in use"""

    def __init__(self, scheduler: AsyncIOScheduler):
        self._scheduler = scheduler
        self._id_generator = token_id_generator()
        self._tokens: Dict[int, Token] = {}

    def get_tokens(self, member: Member, guild: Guild, channel: Optional[TextChannel] = None) -> Set[Token]:
        """Provides all valid tokens for a given user"""

        permission = Permission(guild, channel, set())
        tokens = set()
        for token_id, token in self._tokens.items():
            tokens.add(token_id)
            permission.permissions.update(Permission.from_channel(guild, channel, token.permissions))


    def add_token(self, token: Token, duration: float):
        """Adds a token to be maintained"""
        token_id = next(self._id_generator)
        self._tokens.update({token_id: token})
        self._scheduler.add_job(lambda tid=token_id, *_: self.del_token(tid), seconds=duration)

    def del_token(self, token_id: int):
        """Deletes a token to no longer be maintained"""
        del self._tokens[token_id]
