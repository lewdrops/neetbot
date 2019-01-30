import asyncio

BOTMODE_DELETION_TIME = 3


async def delete_msg_in(message: str, x: int = BOTMODE_DELETION_TIME):
    await asyncio.sleep(x)
    await message.delete()
