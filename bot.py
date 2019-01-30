# std lib

# other libraries
import asyncio
import discord

# project imports
from keys import DISCORD_CLIENT_ID
from utils import msg_to_member
from emojizeMessage import emojize_message
from membership import membership_duration
from chitchat import send_message
from botmode import delete_msg_in, BOTMODE_DELETION_TIME
from dictionary import get_synonyms

# global constants

# setup

client = discord.Client()

# global vars
botmode_members = set()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

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
            await send_message(message, text="bot mode off!")
        else:
            botmode_members.add(target)
            await send_message(message, text="bot mode on!")

    if str(message.author) in botmode_members:
        await delete_msg_in(message)

    if content == "$synonym":
        word = content[content.index(" ")+1:]
        await send_message(message, text=f"looking up {word}...")
        res = get_synonyms(word)
        await send_message(message, ("found: " + ", ".join(res)) if res else "No synonyms found")

client.run(DISCORD_CLIENT_ID)