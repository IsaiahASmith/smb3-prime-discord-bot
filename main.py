from apscheduler.schedulers.asyncio import AsyncIOScheduler
from os import environ

from discord import Intents
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import when_mentioned_or

from database import session, Guild

from core import setup as setup_core
from log import setup as setup_log
from info import setup as setup_info
from translate import setup as setup_translate


VERSION = "0.0.1"
COGS = [setup_core, setup_log, setup_info, setup_translate]


def get_prefix(bot, message):
    guild = session.query(Guild).filter(Guild.guild_id == message.guild.id).first()

    try:
        prefix = guild.prefix
    except AttributeError:
        prefix = "+"
        session.add(Guild(guild_id=message.guild.id, prefix=prefix))
        session.commit()

    if len(prefix) > 5:
        # The prefix got fucked up, fix it
        print("Resetting the prefix")
        guild.prefix = "+"
        session.commit()

    return when_mentioned_or(prefix)(bot, message)


class Bot(BotBase):
    def __init__(self):
        self.version = None
        self.ready = False

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=get_prefix, 
            owner_id=environ['TOKEN'],
            intents=Intents.all()
        )

    def setup(self):
        for cog in COGS:
            cog(self)

    def run(self, version):
        self.version = version

        print("running setup")
        self.setup()

        print("running bot")

        super().run(environ['TOKEN'], reconnect=True)

    async def on_connect(self):
        print(f"We have logged in")

    async def on_disconnect(self):
        print(f"We have logged out")

    async def on_ready(self):
        pass

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)        


if __name__ == "__main__":
    #from keep_alive import keep_alive
    #keep_alive()  # Runs a random server so the bot doesn't go to sleep.

    print("making bot")
    bot = Bot()
    bot.run(VERSION)