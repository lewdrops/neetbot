import random

from discord.ext import commands
from nltk.corpus import wordnet as wn

BLACK_LIST = ["is", "are"]


#
def penn_to_wn(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


def synonyms_of(word):
    # docs: https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
    syns = wn.synsets(word)

    return set(lemma.name() for syn in syns
               for lemma in syn.lemmas())


class NLPCog:
    """testing cogs"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testme(self, ctx, msg):
        print("say it")
        await ctx.send(msg)

    @commands.command()
    async def fancify(self, ctx, *text):
        """substitute fancy words to sound pretentious"""
        fancy_text = []
        for w in text:  # for each word, pick a random synonym if there are any
            synonyms = []
            if w not in BLACK_LIST:
                synonyms += list(synonyms_of(w.lower()))

            fancy_text.append(w if not synonyms else random.choice(synonyms))

        await ctx.send(' '.join(fancy_text))


def setup(bot):
    bot.add_cog(NLPCog(bot))
