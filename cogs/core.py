from database import session, Guild

from discord.ext.commands import Cog, CheckFailure, command, has_permissions


class Core(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new):
        print("new", new)

        if len(new) > 5:
            await ctx.send("The prefix can not be more than five characters in length.")
        else:
            guild = session.query(Guild).filter(Guild.id == ctx.guild.id).first()
            guild.prefix = new
            session.commit()
            await ctx.send(f"Prefix set to {new}.")

    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You need the Manage Message permission to do that.")

    @Cog.listener()
    async def on_ready(self):
        pass

def setup(bot):
    bot.add_cog(Core(bot))