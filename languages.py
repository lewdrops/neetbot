from googletrans import Translator

translator = Translator()


async def translate(message, text, dest="en", src="auto"):
    res = translator.translate(text, dest=dest, src=src)
    print(res, res.src, res.dest, res.text)
    return res

