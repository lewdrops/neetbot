from os import environ
from oxforddictionaries.words import OxfordDictionaries

# from keys import OXDICT_APPID, OXDICT_APPKEY
oxdict = OxfordDictionaries(environ['OXDICT_APPID'], environ['OXDICT_APPKEY'])


def use_oxford(word):
    res = oxdict.get_synonyms(word).json()
    data = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']
    return [s['text'] for s in data]


def get_synonyms(word, task="first", num=1):
    try:
        if True:
            synonyms = use_oxford(word)

        if task == "longest":
            synonyms.sort(key=lambda w: -len(w))

        return synonyms[:num]
    except:
        print("synonym fail!")
        return


# @bot.command()
# async def fancify(ctx, *text):
#     """substitute fancy words to sound pretentious"""
#
#     fancy_text = []
#     for word in text:
#         fancier = get_synonyms(word, "longest")
#         fancy_text.append(fancier[0] if fancier else word)
#     await ctx.send(' '.join(fancy_text))
