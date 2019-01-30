import asyncio


async def greet_back(message):
    print("received a message", '-', message.content, '\n', message)
    msg = await message.channel.send('Hello!')
    await asyncio.sleep(3)
    await msg.delete()
    print("msg deleted!")
