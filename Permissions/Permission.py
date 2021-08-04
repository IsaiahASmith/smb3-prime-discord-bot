from typing import Set

from discord import Guild

from Permissions.PermissionID import PermissionID


class Permission:
    """A series of permissions to provide to a user"""
    def __init__(self, guild: Guild, permissions: Set[PermissionID]):
        self.guild = guild
        self.permissions = permissions

    def __validate__(self, other) -> bool:
        """Determines if a permission actually covers another set of permissions"""
        if not self.guild == other.guild:
            return False
        return other.permissions.issubset(self.permissions)
