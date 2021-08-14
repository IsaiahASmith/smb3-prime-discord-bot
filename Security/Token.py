from dataclasses import dataclass
from typing import Set, Optional

from discord import Member

from Security.Permission import Permission


@dataclass
class Token:
    """An item that allows for a user to achieve a permission otherwise unauthenticated"""
    permissions: Permission
    uses: int = 1
    members: Optional[Set[Member]] = None

    def __contains__(self, item: Member):
        """Returns if a member can use a token"""
        return item in self.members
