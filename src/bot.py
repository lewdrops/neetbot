# std lib
import asyncio
from os import environ

# other libraries
import discord
from discord.ext import commands
import gettext
gettext.install('base', localedir='locale')  # let's do nothing too crazy for now, let's just extract what needs to be translated.

# project imports
# from keys import DISCORD_CLIENT_ID
from utils import msg_to_member, after_space, get_role, toggle_role_for
from emojizeMessage import emojize_message
from membership import membership_duration
from chitchat import send_message, good_bot_reply
from botmode import delete_msg_in
from dictionary import get_synonyms
from languages import translate
from nlp import find_match
from images import image_link_of
from sparql import Sparql

# global constants
MEDIA_PATH = "../media/"

# setup
# client = discord.Client()
bot = commands.Bot(command_prefix='$',
                   description="Halp urself")

# global vars
emoji_dict = {}


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    content = message.content

    if str(message.author) == 'MEE6#4876':  # todo: delete mee6's message if user has been a member for less than two days
        S = content
        if " just left " in S:
            name = S[:S.index(' ')]
            # target = message.guild.get_member_named(name)
            target = bot.users.find(name)
            print(target)

    if message.author in get_role(message, "botmode").members:
        await delete_msg_in(message)

    # if content.startswith("$synonym"):
    #     _, word, task, *_ = content.split() + [None]  # default command is to return a synonym
    #     await send_message(message, text=_("looking up {word}...").format())
    #     res = get_synonyms(word, task)
    #     await send_message(message, "found: {}".format(", ".join(res)) if res else "No synonyms found")

    # if content == _("good bot"):
    #     await good_bot_reply(message)

    if "momoa" in content.lower():
        await send_message(message, "<:momoa:539246620462678027>", 3)

    # preempt translation
    # if False:
    #     translation = await translate(message, content)
    #     if translation.src != "en":
    #         msg = _("`{content}` means \n`{translation.text}`").format
    #         await send_message(message, text=msg)

    await bot.process_commands(message)


@bot.command(aliases=["membership-duration"])
async def membership(ctx, arg):
    """How long a user has been a guild member"""

    target = msg_to_member(ctx.message)
    reply = membership_duration(target)
    await ctx.message.channel.send(reply)


# delete every msg by user after a few secs
@bot.command(aliases=["toggle-botmode"])
async def botmode(ctx):
    """In botmode, commands and replies auto-delete after a while"""
    await toggle_role_for(ctx, "botmode", ("bot mode on!", "bot mode off!"))


@bot.command(aliases=["list-emojis"])
async def emojis(ctx):
    """lists the guild's emojis"""
    await ctx.send(' '.join(str(e) for e in ctx.message.guild.emojis))


@bot.command(aliases=["toggle-emojify"])
async def emojify(ctx):
    """toggles 'emojifier' role, where botty react to what you say with emojis"""
    await toggle_role_for(ctx, "emojifier", ("ONE OF US!", f"ET TU, {ctx.message.author.name}...?"))


@bot.command()
async def fancify(ctx, *text):
    """substitute fancy words to sound pretentious"""

    fancy_text = []
    for word in text:
        fancier = get_synonyms(word, "longest")
        fancy_text.append(fancier[0] if fancier else word)
    await send_message(ctx.message, ' '.join(fancy_text))


@bot.command(aliases=["translate"])
async def trans(ctx, text):
    """google translates to english"""
    await ctx.send((await translate(ctx.message, text)).text)


@bot.command(aliases=["picture", "pic-of"])
async def pic(ctx, keyword):
    """embed a pic from google images for the keyword"""

    e = discord.Embed()
    e.set_image(url=await image_link_of(keyword))
    await ctx.message.channel.send(embed=e)


@bot.command(aliases=["gif-of"])
async def gif(ctx, keyword):
    """embed a gif from google images for the keyword"""

    e = discord.Embed()
    e.set_image(url=await image_link_of(keyword, format="gif"))
    await ctx.message.channel.send(embed=e)


@bot.command(aliases=["we"])
async def word_equation(ctx, *words):
    matches = find_match(''.join(words))
    await ctx.send(f"`{' '.join(words)}` is {matches[0][0]}")


@bot.command()
async def sparql(ctx, *text):
    ctx.send(_("Your results are as follows.\n"
               "```\n"
               "{result}"
               "```\n").format(result=Sparql(text[0], text[1:])))

bot.run(environ['DISCORD_BOT_TOKEN'])
