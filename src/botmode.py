# todo: delete bot's own replies in botmode
import asyncio

BOTMODE_DELETION_TIME = 3


async def delete_msg_in(message, seconds=BOTMODE_DELETION_TIME):
    await asyncio.sleep(seconds)
    await message.delete()
