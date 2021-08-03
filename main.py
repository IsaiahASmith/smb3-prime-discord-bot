from apscheduler.schedulers.asyncio import AsyncIOScheduler
from os import environ

from discord import Intents, TextChannel
from discord.ext.commands import Bot as BotBase

from cogs.core import setup as setup_core
from cogs.log import setup as setup_log
from cogs.sender import setup as setup_sender
from cogs.options import setup as setup_options
from cogs.info import setup as setup_info
from cogs.channel_manager import setup as channel_manager_setup
from cogs.translate import setup as setup_translate
from cogs.security import setup as setup_security

from prefix import get_prefix, prefix


VERSION = "0.0.1"
COGS = [
    (setup_core, "core"),
    (setup_log, "log"),
    (setup_sender, "sender"),
    (setup_options, "options"),
    (setup_info, "info"),
    (channel_manager_setup, "channel_manager"),
    (setup_translate, "translate"),
    (setup_security, "security")
]


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
        for (cog, name) in COGS:
            c = cog(self)
            self.cogs_lookup.update({name: c})

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

        if message.author.bot or message.content.startswith(prefix(message.guild)):
            return

        if isinstance(message.channel, TextChannel):
            # This message is part of a conversation from the members
            self.dispatch("on_conversation", message)


if __name__ == "__main__":
    #from keep_alive import keep_alive
    #keep_alive()  # Runs a random server so the bot doesn't go to sleep.

    # Download some random thing nltk needs
    import nltk
    nltk.download('punkt')

    print("making bot")
    bot = Bot()
    bot.run(VERSION)