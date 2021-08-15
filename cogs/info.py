from typing import Optional
from datetime import datetime

from discord import Embed, Member

from discord.ext.commands import Cog, command


class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="userinfo", aliases=["ui"])
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        embed = Embed(title="User Information", colour=target.colour, timestamp=datetime.utcnow())

        fields = [
            ("ID", target.id, False),
            ("Name", str(target), True),
            ("Bot", target.bot, True),
            ("Role", target.top_role.mention, True),
            ("Status", str(target.status).title(), True),
            ("Created", target.created_at.strftime("%m/%d/%Y %H:%M:%S"), True),
            ("Joined", target.joined_at.strftime("%m/%d/%Y %H:%M:%S"), True),
            ("Boosted", bool(target.premium_since), True),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=target.avatar_url)

        await ctx.send(embed=embed)

    @command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
    async def server_info(self, ctx):
        embed = Embed(title="Server Information", colour=ctx.guild.owner.colour, timestamp=datetime.utcnow())

        statuses = [
            len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members))),
        ]

        fields = [
            ("ID", ctx.guild.id, False),
            ("Owner", ctx.guild.owner, True),
            ("Region", ctx.guild.region, True),
            ("Created", ctx.guild.created_at.strftime("%m/%d/%Y %H:%M:%S"), True),
            ("Members", len(ctx.guild.members), True),
            ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
            ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
            (
                "Statuses",
                f":green_circle: {statuses[0]}, :orange_circle:{statuses[1]}, :red_circle:{statuses[2]}, :white_circle:{statuses[3]}",
                True,
            ),
            ("Text Channels", len(ctx.guild.text_channels), True),
            ("Voice Channels", len(ctx.guild.voice_channels), True),
            ("Categories", len(ctx.guild.categories), True),
            ("Roles", len(ctx.guild.roles), True),
            ("Invites", len(await ctx.guild.invites()), True),
            ("\u200b", "\u200b", True),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)


def setup(bot):
    cog = Info(bot)
    bot.add_cog(cog)
    return cog
