from discord import Emoji
from discord.utils import get

emoji_names = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"
]


def get_emoji(guild, emoji_name) -> Emoji:
    return get(guild.emojis, name=emoji_name)