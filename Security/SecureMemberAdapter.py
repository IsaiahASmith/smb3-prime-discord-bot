from discord import Member, TextChannel, Guild
from discord.ext.commands import Context

from Security.Permission.Permission import Permission


class SecureMemberAdapter:
    """Attaches additional functionality related to security to members"""

    def __init__(self, member: Member, channel: TextChannel, guild: Guild):
        self.member = member
        self.channel = channel
        self.guild = guild

    @property
    def permissions(self) -> Permission:
        return Permission.from_discord_permissions(
            guild=self.guild, channel=self.channel, permissions=self.channel.permissions_for(self.member)
        )