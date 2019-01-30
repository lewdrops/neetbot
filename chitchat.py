import random

import asyncio

GOOD_BOT_REPLIES = ["That's what you are, but what am I?",
                    "No, I am Great Bot",
                    "B-baka!"]


async def send_message(message, text="Hello!", delete_in=False):
    print("received a message", '-', message.content, '\n', message)
    msg = await message.channel.send(text)

    if delete_in:
        await asyncio.sleep(delete_in)
        await msg.delete()


async def good_bot_reply(message):
    reply = random.choice(GOOD_BOT_REPLIES)
    await send_message(message, text=reply)
