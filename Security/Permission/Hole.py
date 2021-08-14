from dataclasses import dataclass
from typing import Set, Optional, Any

from bcrypt import checkpw, hashpw, gensalt
from discord import Member

from Security.Permission import Permission
from Security.Permission.TokenInvalidatedException import TokenInvalidatedException
from Security.Permission.AccessDeniedException import AccessDeniedException


@dataclass
class Hole:
    """A hole that commands can be used to achieve otherwise unauthorized commands"""
    permissions: Permission
    uses: int = 1
    members: Optional[Set[Member]] = None
    password_hash: Optional[bytes] = None
    content: Optional[Any] = None

    @classmethod
    def from_password(
            cls,
            permissions: Permission,
            uses: int = 1,
            members: Optional[Set[Member]] = None,
            password: Optional[str] = None,
            content: Optional[Any] = None
    ):
        if password is None:
            return cls(permissions, uses, members, password, content)
        return cls(permissions, uses, members, hashpw(password.encode("utf-8"), gensalt()), content)

    def verify_member(self, member: Optional[Member]):
        """Verifies the member or raises an error"""
        if member is None:
            raise AccessDeniedException(hole=self, message="Access Denied - No member provided")
        if member not in self.members:
            raise AccessDeniedException(hole=self, message=f"Access Denied - {member} does not have permission")

    def verify_password(self, password: Optional[str]):
        """Verifies the password or raises an error"""
        if password is None:
            raise AccessDeniedException(hole=self, message="Access Denied - No password provided")
        if not checkpw(password.encode("utf-8"), self.password_hash):
            raise AccessDeniedException(hole=self, message="Access Denied - Password incorrect")

    def validate(self, member: Optional[Member] = None, password: Optional[str] = None):
        if not self.uses:
            raise TokenInvalidatedException(hole=self, message="Token Invalid - No more uses")
        if self.members is not None:
            self.verify_member(member)
        if self.password_hash is not None:
            self.verify_password(password)
        self.uses -= 1

    def get_content(self, member: Optional[Member] = None, password: Optional[str] = None):
        self.validate(member, password)
        return self.content

    def use(self, member: Optional[Member] = None, password: Optional[str] = None) -> bool:
        """Determines if a user can use a certain permission"""
        self.validate(member, password)
