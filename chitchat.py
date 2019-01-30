import asyncio


async def send_message(message, text="Hello!", delete_in=False):
    print("received a message", '-', message.content, '\n', message)
    msg = await message.channel.send(text)
    if delete_in:
        await asyncio.sleep(delete_in)
        await msg.delete()
