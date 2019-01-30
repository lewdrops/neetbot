import asyncio


async def greet_back(message, text="Hello!"):
    print("received a message", '-', message.content, '\n', message)
    msg = await message.channel.send(text)
    await asyncio.sleep(3)
    await msg.delete()
    print("msg deleted!")
