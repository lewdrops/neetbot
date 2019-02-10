from googletrans import Translator

from bot_constants import HR

translator = Translator()


async def translate(message, text, dest="en", src="auto"):
    res = translator.translate(text, dest=dest, src=src)
    print(f"translating {res.src} ⇒ {res.dest}"
          f"\n'{text}' ⇒ '{res.text}'{HR}")
    return res

