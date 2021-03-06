# std lib
import asyncio
from os import environ
import sys
import traceback

# other libraries
import discord
from discord.ext import commands
import gettext
gettext.install('base', localedir='locale')  # let's do nothing too crazy for now, let's just extract what needs to be translated.

# project imports
# from keys import DISCORD_CLIENT_ID
from bot_constants import MEDIA_PATH, COMMAND_PREFIX, HR
from utils import msg_to_member, after_space, \
    get_role, toggle_role_for, create_roles_if_needed, has_role
from membership import membership_duration
from botmode import delete_msg_in
from dictionary import get_synonyms
from nlp import find_match
from sparql import Sparql

from cogs.chitchat import send_message, process_reply
from cogs.reactions import emojize_message
from cogs.languages import translate

# setup
# client = discord.Client()
bot = commands.Bot(command_prefix=COMMAND_PREFIX,
                   description="Halp urself")

startup_extensions = ["cogs.images", "cogs.reactions", "cogs.languages", "cogs.natlang"]

# global vars
emoji_dict = {}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} "
          f"with access to: \n {' & '.join(str(g) for g in bot.guilds)}{HR}")

    for guild in bot.guilds:
        await create_roles_if_needed(guild, "emojifier", "botmode", "autotranslate")


@bot.event
async def on_message(message):
    content, guild, author = message.content, message.guild, message.author

    # ignore own messages as well as those without text
    if message.author == bot.user or not content:
        return

    print(f"got a message: {content}")

    if await has_role(message, "botmode"):
        await delete_msg_in(message)

    if content[0] != COMMAND_PREFIX:

        # consider clever replies
        await process_reply(message)

        # add reactions if author is an emojifier
        if await has_role(message, "emojifier"):
            await emojize_message(message)

        # detect & translate non-english phrases
        if await has_role(message, "autotranslate"):
            translation = await translate(message, content)
            if translation.src != "en":
                msg = f"```⇒ {translation.text}```"
                await send_message(message, text=msg)
    else:
        await bot.process_commands(message)


@bot.command(aliases=["membership-duration"])
async def membership(ctx, arg):
    """How long a user has been a guild member"""

    target = msg_to_member(ctx.message)
    reply = membership_duration(target)
    await ctx.send(reply)


# delete every msg by user after a few secs
@bot.command(aliases=["bm", "toggle-botmode"])
async def botmode(ctx):
    """In botmode, commands and replies auto-delete after a while"""
    await toggle_role_for(ctx, "botmode", ("bot mode on!", "bot mode off!"))


@bot.command(aliases=["we"])
async def word_equation(ctx, *words):
    matches = find_match(''.join(words))
    await ctx.send(f"`{' '.join(words)}` is {matches[0]}")


@bot.command()
async def sparql(ctx, *text):
    ctx.send(_("Your results are as follows.\n"
               "```\n"
               "{result}"
               "```\n").format(result=Sparql(text[0], text[1:])))


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

    bot.run(environ['DISCORD_BOT_TOKEN'], bot=True, reconnect=True)
