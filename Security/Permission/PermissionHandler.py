from typing import Dict, Union

from .Permission import Permission


class PermissionHandler:
    """Finds the given permissions of a user and contains them for their respective"""

    def __init__(self, permission: Permission, children: Dict[int, "PermissionHandler"]):
        self.permission = permission
        self.children = children

    @property
    def permissions(self) -> Dict[int, Union["PermissionHandler", Permission]]:
        """Finds all valid permission of itself and its children"""
        return {0: self.permission, **self.children}

    def __bool__(self) -> bool:
        return all(bool(permission) for permission in self.permissions.values())

    def __and__(self, other):
        children_keys = set(self.children.keys()).intersection(other.children.keys())

        return PermissionHandler(
            self.permission & other.permissions,
            {key: self.children[key] & other.children[key] for key in children_keys}
        )

    def __iand__(self, other):
        children_keys = set(self.children.keys()).intersection(other.children.keys())

        self.permission &= other.permissions
        for key in children_keys:
            self.children[key] &= other.children[key]

        return self

    def __or__(self, other):
        return Permission(self.permissions | other.permissions)

    def __ior__(self, other):
        self.permissions |= other.permissions
        return self

    def __add__(self, other):
        return Permission(self.permissions + other.permissions)

    def __iadd__(self, other):
        self.permissions += other.permissions
        return self

    def __sub__(self, other):
        return Permission(self.permissions - other.permissions)

    def __isub__(self, other):
        self.permissions -= other.permissions
        return self

    def __lt__(self, other):
        return self.permissions < other.permissions

    def __le__(self, other):
        return self.permissions <= other.permissions

    def __eq__(self, other):
        return self.permissions == other.permissions

    def __ne__(self, other):
        return self.permissions != other.permissions

    def __ge__(self, other):
        return self.permissions >= other.permissions


"""
if regs == regs & user_perms:
    return True

tokens = get_user_tokens(user)
used_tokens = set()
unresolved = regs - user_perms
for id, token in tokens:
    if token.perms & unresolved:
        use(token)
        unresolved -= token.perms
        if not unresolved:
            return True
return False

This is a comment, not code


"""