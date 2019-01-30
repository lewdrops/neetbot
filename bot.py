# std lib

# other libraries
import asyncio
import discord

# project imports
from keys import CLIENT_ID
from utils import msg_to_member
from emojizeMessage import emojize_message
from membership import membership_duration
from chitchat import greet_back
from botmode import delete_msg_in, BOTMODE_DELETION_TIME

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

    if message.content.startswith('$hello'):
        await greet_back(message)

    if str(message.author) == 'lastdrop#6308':
        await emojize_message(message)
    elif str(message.author) == 'MEE6#4876':  # todo: delete mee6's message if user has been a member for less than two days
        S = message.content
        if " just left " in S:
            name = S[:S.index(' ')]
            # target = message.guild.get_member_named(name)
            target = client.users.find(name)
            print(target)

    if message.content.startswith('$join'):
        target = msg_to_member(message)
        reply = membership_duration(target)
        msg = await message.channel.send(reply)

    # delete every msg by user after a few secs
    if message.content == "$botmode":
        target = str(message.author)
        if target in botmode_members:
            botmode_members.remove(target)
            await greet_back(message, text="bot mode off!")
        else:
            botmode_members.add(target)
            await greet_back(message, text="bot mode on!")

    if str(message.author) in botmode_members:
        await delete_msg_in(message)

client.run(CLIENT_ID)