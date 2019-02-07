import random

import asyncio

GOOD_BOT_REPLIES = [_("That's what you are, but what am I?"),  # these replies are going to be defined only once, in one language
                    _("No, I am Great Bot"),
                    _("B-baka!")]


async def send_message(message, text=_("Hello!"), delete_in=False):  # Note: this translation will be evaluated at initialization
    print(_("received a message"), '-', message.content, '\n', message)

    msg = await message.channel.send(text)

    if delete_in:
        await asyncio.sleep(delete_in)
        await msg.delete()


async def good_bot_reply(message):
    reply = random.choice(GOOD_BOT_REPLIES)
    await send_message(message, text=reply)
