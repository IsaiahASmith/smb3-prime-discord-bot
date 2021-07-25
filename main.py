from apscheduler.schedulers.asyncio import AsyncIOScheduler
from os import environ

from discord import Intents
from discord.ext.commands import Bot as BotBase

from cogs.core import setup as setup_core
from cogs.log import setup as setup_log
from cogs.options import setup as setup_options
from cogs.info import setup as setup_info
from cogs.channel_manager import setup as channel_manager_setup
from cogs.translate import setup as setup_translate
from cogs.security import setup as setup_security

from prefix import get_prefix


VERSION = "0.0.1"
COGS = [setup_core, setup_log, setup_options, setup_info, channel_manager_setup, setup_translate, setup_security]


class Bot(BotBase):
    def __init__(self):
        self.version = None
        self.ready = False
        self.cogs_lookup = {}

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=get_prefix, 
            owner_id=environ['TOKEN'],
            intents=Intents.all()
        )

    def setup(self):
        for cog in COGS:
            c = cog(self)
            self.cogs_lookup.update({c.__class__.__name__: c})

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