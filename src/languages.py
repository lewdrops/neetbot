from googletrans import Translator

translator = Translator()


async def translate(message, text, dest="en", src="auto"):
    res = translator.translate(text, dest=dest, src=src)
    print(f"translating {res.src} ⇒ {res.dest}"
          f"\n'{text}' ⇒ '{res.text}'")
    return res

