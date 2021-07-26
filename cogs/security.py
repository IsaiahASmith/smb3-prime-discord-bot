from typing import Set

from discord import Member
from discord.ext.commands import Cog

from bcrypt import hashpw, gensalt, checkpw


def generate_password(password: str) -> bytes:
    """Provides a salted hash from a password"""
    return hashpw(password.encode("utf-8"), gensalt())


class Security(Cog):
    _id_count = 0

    def __init__(self, bot):
        self.bot = bot
        self._pending_holes = {}

    async def open_hole(self, members: Set[Member], password: str, *args) -> int:
        """Provides an id to check against"""
        cur_id = self._id_count
        self._pending_holes.update({cur_id: (members, generate_password(password), *args)})
        self._id_count += 1
        return cur_id

    async def close_hole(self, hole_id: int):
        """Removes a hole the check against"""
        del self._pending_holes[hole_id]

    async def get_hole_info(self, hole_id: int, member: Member, password: str):
        if await self.check_hole(hole_id, member, password):
            return list(self._pending_holes[hole_id])[2:]  # Remove the members and password from the hole

    async def check_hole(self, hole_id: int, member: Member, password: str) -> bool:
        """Allows processing through a hole with a valid hole, member, and password"""
        if hole_id not in self._pending_holes:
            return False

        hole = self._pending_holes[hole_id]
        if member not in hole[0]:
            return False

        return checkpw(password.encode("utf-8"), hole[1])


def setup(bot):
    cog = Security(bot)
    bot.add_cog(cog)
    return cog
