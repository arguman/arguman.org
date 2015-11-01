from textblob import TextBlob, Word
from operator import or_


def noun_phrases(text):
    blob = TextBlob(text)
    return blob.tokenize()


def get_synsets(text):
    return Word(to_lemma(text)).synsets


def get_lemmas(text):
    word = Word(to_lemma(text))
    sets = map(set, [synset.lemma_names()
                     for synset in word.synsets])

    return map(from_lemma, reduce(or_, sets))


def to_lemma(text):
    return text.replace(' ', '_')


def from_lemma(text):
    return text.replace('_', ' ')


def tokenize(text):
    blob = TextBlob(text.lower())
    return blob.tokenize()

def is_subsequence(sequence, parent):
    for i in xrange(1 + len(parent) - len(sequence)):
        if sequence == parent[i:i+len(sequence)]:
            return True
    return False
