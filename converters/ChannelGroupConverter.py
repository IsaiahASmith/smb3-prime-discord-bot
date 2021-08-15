from typing import Optional, List

from discord.ext.commands import Converter, CommandError

from Option import Option
from Response import Response
from emojis import emoji_names, get_emoji
from cogs.options import Options
from database import ChannelGroup, session


def validate_guild_from_similar_name(name: str, guild_id: int) -> Optional[List[ChannelGroup]]:
    """Tries to find groups with a similar name or None with respect to to permission"""
    return [
        session.query(ChannelGroup).filter(
            group for group in (ChannelGroup.guild_id == guild_id) & (ChannelGroup.name.ilike(f"%{name}%"))
        )
    ]


def validate_guild_from_name(name: str, guild_id: int) -> Optional[List[ChannelGroup]]:
    """Tries to find groups with valid names or None with respect to permission"""
    groups = [
        group
        for group in session.query(ChannelGroup).filter(
            (ChannelGroup.guild_id == guild_id) & (ChannelGroup.name == name)
        )
    ]

    if len(groups) == 0:
        # Try a broader search
        return validate_guild_from_similar_name(name, guild_id)
    return groups


class ChannelGroupConverter(Converter):
    """Tries and finds a valid ChannelGroup"""

    async def convert(self, ctx, argument) -> Optional[ChannelGroup]:
        try:
            group_id = int(argument)
        except ValueError:
            groups = validate_guild_from_name(argument, ctx.guild.id)
            if groups is None:
                raise CommandError(f"Group was unable to be found with name: {argument!s}")
            elif len(groups) == 1:
                group_id = groups[0].id
            elif len(groups) < 11:
                option_cog: Options = ctx.bot.cogs_lookup["options"]
                option = Option(
                    question="Select the channel group desired.",
                    description="React with the corresponding emoji",
                    colour=ctx.author.colour,
                    responses=[
                        Response(group.name, f":{emoji_names[idx]}:", get_emoji(ctx.guild, emoji_names[idx]))
                        for idx, group in enumerate(groups)
                    ],
                    responders={ctx.author},
                )
                selected_option = await option_cog.ask_for_options(ctx, option)
                group_id = groups[selected_option].id
            else:
                raise CommandError(f"To many groups found.")
        group = session.query(ChannelGroup).filter(ChannelGroup.id == group_id).first()
        return group
