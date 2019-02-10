# todo: have high confidence target lang is not english before translating!
from discord.ext import commands
from googletrans import Translator

from bot_constants import HR
from utils import toggle_role_for

translator = Translator()


async def translate(message, text, dest="en", src="auto"):
    res = translator.translate(text, dest=dest, src=src)
    print(f"translating {res.src} ⇒ {res.dest}"
          f"\n'{text}' ⇒ '{res.text}'{HR}")
    return res


class LanguageCog:
    """Translation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["tr", "translate"])
    async def trans(self, ctx, text):
        """google translates to english"""
        await ctx.send((await translate(ctx.message, text)).text)

    @commands.command(aliases=["tt", "toggle-autotranslate"])
    async def autotranslate(self, ctx):
        """toggles auto-translate function of bot"""
        await toggle_role_for(ctx, "autotranslate", ("I'll now translate everything you say to english!",
                                                     "I'll stop translating everything you say to english!"))


def setup(bot):
    bot.add_cog(LanguageCog(bot))
