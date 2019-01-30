from emoji import emojize


async def emojize_message(message):
    words = message.content.lower().split()
    seen = set()

    for word in words:
        if word not in seen:
            seen.add(word)
            emoji = emojize(f':{word}:', use_aliases=True)
            if not emoji.startswith(':'):
                await message.add_reaction(emoji)
                print("reactions added!")
