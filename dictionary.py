from oxforddictionaries.words import OxfordDictionaries

from keys import OXDICT_APPID, OXDICT_APPKEY

oxdict = OxfordDictionaries(OXDICT_APPID, OXDICT_APPKEY)


def get_synonyms(word, num=1):
    try:
        res = oxdict.get_synonyms(word).json()
        data = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']
        synonyms = [s['text'] for s in data[:num]]
        return synonyms
    except:
        print("synonym fail!")
        return
