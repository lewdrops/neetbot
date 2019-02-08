import re

import gensim
from nltk.stem.snowball import SnowballStemmer

WORD2VEC_WEIGHTS = '../word2vec/GoogleNews-vectors-negative300.bin'

if False:
    model = gensim.models.KeyedVectors.load_word2vec_format(WORD2VEC_WEIGHTS, binary=True)

stemmer = SnowballStemmer('english')


def similar_words_for(positive, negative, limit):
    inputs = {stemmer.stem(x) for x in positive + negative}
    words = model.most_similar(positive=positive, negative=negative, topn=limit)
    print(words)
    return [w[0] for w in words if stemmer.stem(w[0]) not in inputs]


def find_match(text):
    parts = re.split('(\W+)', text.lower().replace(' ', ''))
    positives = [parts[0]]
    negatives = []
    for i in range(1, len(parts), 2):
        (positives if parts[i] == '+' else negatives).append(parts[i+1])
    print(positives, negatives)
    return similar_words_for(positives, negatives, 30)
