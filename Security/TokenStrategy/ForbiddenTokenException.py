from discord import Member

from Security.Permission import Permission


class ForbiddenTokenException(Exception):
    """
    An error that is raised when the author of a token tries to generate a token where they do no have permissions.
    """

    def __init__(
            self,
            author: Member,
            permissions_supplied: Permission,
            author_permissions: Permission,
    ):
        self.author = author
        self.permissions_supplied = permissions_supplied
        self.author_permissions = author_permissions
        super().__init__(
            f"{self.author} does not have {self.permissions_supplied}, only {self.author_permissions}"
        )