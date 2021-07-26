from discord.ext.commands import when_mentioned_or

from database import session, Guild


def prefix(guild) -> str:
    guild = session.query(Guild).filter(Guild.id == guild.id).first()
    return guild.prefix


def get_prefix(bot, message):
    guild = session.query(Guild).filter(Guild.id == message.guild.id).first()

    try:
        prefix = guild.prefix
    except AttributeError:
        prefix = "+"
        session.add(Guild(id=message.guild.id, prefix=prefix))
        session.commit()

    if len(prefix) > 5:
        # The prefix got fucked up, fix it
        print("Resetting the prefix")
        guild.prefix = "+"
        session.commit()

    return when_mentioned_or(prefix)(bot, message)