# std lib
import asyncio

# other libraries
import discord
import gettext
gettext.install('base', localedir='locale')  # let's do nothing too crazy for now, let's just extract what needs to be translated.

# project imports
from keys import DISCORD_CLIENT_ID
from utils import msg_to_member, after_space
from emojizeMessage import emojize_message
from membership import membership_duration
from chitchat import send_message, good_bot_reply
from botmode import delete_msg_in
from dictionary import get_synonyms
from languages import translate
from images import image_link_of

# global constants

# setup
client = discord.Client()

# global vars
botmode_members = set()
emoji_dict = {}

# functions


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    content = message.content

    if str(message.author) == 'lastdrop#6308':
        await emojize_message(message)
    elif str(message.author) == 'MEE6#4876':  # todo: delete mee6's message if user has been a member for less than two days
        S = content
        if " just left " in S:
            name = S[:S.index(' ')]
            # target = message.guild.get_member_named(name)
            target = client.users.find(name)
            print(target)

    if content.startswith('$join'):
        target = msg_to_member(message)
        reply = membership_duration(target)
        msg = await message.channel.send(reply)

    # delete every msg by user after a few secs
    if content == "$botmode":
        target = str(message.author)
        if target in botmode_members:
            botmode_members.remove(target)
            await send_message(message, text=_("bot mode off!"))
        else:
            botmode_members.add(target)
            await send_message(message, text=_("bot mode on!"))

    if str(message.author) in botmode_members:
        await delete_msg_in(message)

    if content.startswith("$synonym"):
        _, word, task, *_ = content.split() + [None]  # default command is to return a synonym
        await send_message(message, text=_("looking up {word}...").format())
        res = get_synonyms(word, task)
        await send_message(message, "found: {}".format(", ".join(res)) if res else "No synonyms found")

    if content.startswith("$fancify"):
        _, *text = content.split()
        fancy_text = []
        for word in text:
            fancier = get_synonyms(word, "longest")
            fancy_text.append(fancier[0] if fancier else word)
        await send_message(message, ' '.join(fancy_text))

    # if content == _("good bot"):
    #     await good_bot_reply(message)

    if "momoa" in content.lower():
        await send_message(message, "<:momoa:539246620462678027>", 3)

    if content == "$listemojis":
        emoji_list = message.guild.emojis
        emojis = ' '.join(str(e) for e in emoji_list)
        print(emojis)
        await send_message(message, emojis)

    if content.startswith("$trans"):
        print(after_space(content))
        await translate(message, after_space(content))

    # preempt translation
    if len(content) > 4:
        translation = await translate(message, content)
        if translation.src != "en":
            msg = _("`{content}` means \n`{translation.text}`").format
            await send_message(message, text=msg)

    if content.startswith("$pic"):
        link = image_link_of()
        file = discord.File("./media/doggo.jpg", filename="pic.png")
        await message.channel.send("pic.png", file=file)
        await message.channel.send("https://www.catster.com/wp-content/uploads/2017/08/A-fluffy-cat-looking-funny-surprised-or-concerned.jpg")
        # await client.send_file(message.channel, link)

client.run(DISCORD_CLIENT_ID)
