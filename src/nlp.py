import gensim

WORD2VEC_WEIGHTS = '../word2vec/GoogleNews-vectors-negative300.bin'

if False:
    model = gensim.models.KeyedVectors.load_word2vec_format(WORD2VEC_WEIGHTS, binary=True)

import re


def similar_words_for(positive, negative, limit):
    words = model.most_similar(positive=positive, negative=negative, topn=limit)
    print(words)
    return words


def find_match(text):
    parts = re.split('(\W+)', text.replace(' ', ''))
    positives = [parts[0]]
    negatives = []
    for i in range(1, len(parts), 2):
        (positives if parts[i] == '+' else negatives).append(parts[i+1])
    print(positives, negatives)
    return similar_words_for(positives, negatives, 10)
