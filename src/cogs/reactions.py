from discord.ext import commands
from emoji import emojize

from utils import toggle_role_for

BLACKLIST = {"a", "on"}


async def emojize_message(message):
    words = message.content.lower().split()
    seen = set()

    for word in words:
        if word not in seen | BLACKLIST:
            seen.add(word)
            emoji = emojize(f':{word}:', use_aliases=True)
            if not emoji.startswith(':'):
                await message.add_reaction(emoji)


class ReactionsCog:
    """Emojis & reactions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["em", "list-emojis"])
    async def emojis(self, ctx):
        """lists the guild's emojis"""
        await ctx.send("Server emojis:\n\n" + ' '.join(str(e) for e in ctx.message.guild.emojis))

    @commands.command(aliases=["te", "toggle-emojify"])
    async def emojify(self, ctx):
        """toggles 'emojifier' role, where botty react to what you say with emojis"""
        await toggle_role_for(ctx, "emojifier", ("ONE OF US!", f"ET TU, {ctx.message.author.name}...?"))


def setup(bot):
    bot.add_cog(ReactionsCog(bot))
