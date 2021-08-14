from Security.Permission import Permission
from Security.SecureMemberAdapter import SecureMemberAdapter


class NonMemberTokenException(Exception):
    """
    An error that is raised when no members are provided.
    """

    def __init__(
            self,
            secure_member: SecureMemberAdapter,
            permissions: Permission,
            uses: int = 1,
            duration: float = 60.0
    ):
        self.secure_member = secure_member
        self.permissions = permissions
        self.uses = uses
        self.duration = duration
        super().__init__(
            f"{self.secure_member} did not provide any members for their token with "
            f"permissions: {self.permissions}, {self.uses} uses, and a duration of {self.duration}"
        )