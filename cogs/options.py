from typing import Optional

from discord.ext.commands import Cog

from Option import Option


class Options(Cog):
    option_count = 0

    def __init__(self, bot):
        self.bot = bot
        self.pending_options = {}

    async def add_option(self, option: Option) -> int:
        """Adds an option with a set of responses"""
        option_id = self.option_count
        self.pending_options.update({option_id: option})
        self.option_count += 1
        return option_id

    async def ask_for_options(self, ctx, option: Option) -> Optional[int]:
        option_id = await self.add_option(option)
        message = await ctx.channel.send(embed=option.to_embed())
        emojis_to_response = {response.emoji: idx for idx, response in enumerate(option.responses)}
        result = None

        def check(payload) -> bool:
            if payload.message_id == message.id and payload.user_id in option.responders:
                # We are receiving a valid response
                print("validating emoji")
                if payload.emoji in emojis_to_response:
                    nonlocal result
                    result = emojis_to_response[payload.emoji]
                    return True
            return False

        try:
            await self.bot.wait_for('raw_reaction_add', timeout=60.0, check=check)
        except TimeoutError:
            del self.pending_options[option_id]
            await ctx.channel.send("Timeout")
            return None
        return result

    @Cog.listener()
    async def on_ready(self):
        pass


def setup(bot):
    bot.add_cog(Options(bot))
