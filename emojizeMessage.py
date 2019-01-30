from emoji import emojize


async def emojize_message(message):
    words = set(message.content.lower().split())
    for word in words:
        emoji = emojize(f':{word}:')
        if not emoji.startswith(':'):
            await message.add_reaction(emoji)
            print("reactions added!")
