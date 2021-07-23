from apscheduler.schedulers.asyncio import AsyncIOScheduler
from os import environ

from discord import Intents
from discord.ext.commands import Bot as BotBase

import database

from info import setup as setup_info
from translate import setup as setup_translate


VERSION = "0.0.1"
PREFIX = "+"
COGS = [setup_info, setup_translate]


class Bot(BotBase):
    def __init__(self):
        self.prefix = PREFIX
        self.version = None
        self.ready = False

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=PREFIX, 
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