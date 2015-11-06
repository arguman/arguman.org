# -*- coding:utf-8 -*-
import operator
import string
import operator
import itertools

import snowballstemmer
from textblob import TextBlob, Word

LOWER_MAP = {
    'tr': {
        ord('I'): u'ı'
    }
}

STEMMERS = {
    'en': snowballstemmer.stemmer('english'),
    'tr': snowballstemmer.stemmer('turkish'),
}


def noun_phrases(text):
    blob = TextBlob(text)
    return blob.tokenize()


def get_synsets(text):
    return Word(to_lemma(text)).synsets


def get_lemmas(text):
    word = Word(to_lemma(text))
    sets = map(set, [synset.lemma_names()
                     for synset in word.synsets])

    return map(from_lemma, reduce(operator.or_, sets))


def to_lemma(text):
    return text.replace(' ', '_')


def from_lemma(text):
    return text.replace('_', ' ')


def stem_word(word, language):
    stemmer = STEMMERS.get(language)

    if stemmer is None:
        return word

    return (stemmer
            .stemWord(word)
            .strip(string.punctuation))


def tokenize(wordlist, language, stem=True):
    return ' '.join((stem_word(word, language) if stem else word)
                    for word in wordlist)


def lower(text, language):
    if language in LOWER_MAP:
        text = text.translate(LOWER_MAP[language])
    return text.lower()


def build_ngrams(text, language='en'):
    blob = TextBlob(lower(text, language))
    ngrams = [blob.ngrams(n=n) for n in (3, 2, 1)]
    wordlists = reduce(operator.add, ngrams)
    tokenized = (
        tokenize(wordlist, language, stem=True)
        for wordlist in wordlists)
    pure = (
        tokenize(wordlist, language, stem=False)
        for wordlist in wordlists)
    return itertools.chain(tokenized, pure)


def is_subsequence(sequence, parent):
    for i in xrange(1 + len(parent) - len(sequence)):
        if sequence == parent[i:i + len(sequence)]:
            return True
    return False
