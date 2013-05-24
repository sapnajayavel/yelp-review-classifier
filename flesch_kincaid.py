# Calculate Flesch-Kincaid reading level of text
# Adapted from http://acdx.net/calculating-the-flesch-kincaid-level-in-python/

from __future__ import division
import re

def mean(seq):
    return sum(seq) / len(seq)

def syllables(word):
    if len(word) <= 3:
        return 1

    word = re.sub(r"(es|ed|(?<!l)e)$", "", word)
    return len(re.findall(r"[aeiouy]+", word))

terminators = ".!?:;"
def normalize(text):
    term = re.escape(terminators)
    text = re.sub(r"[^%s\sA-Za-z]+" % term, "", text)
    text = re.sub(r"\s*([%s]+\s*)+" % term, ". ", text)
    return re.sub(r"\s+", " ", text)

def text_stats(text):
    text = normalize(text)
    stcs = [s.split(" ") for s in text.split(". ")]
    stcs = filter(lambda s: len(s) >= 2, stcs)

    words = sum(len(s) for s in stcs)
    sbls = sum(syllables(w) for s in stcs for w in s)

    return len(stcs), words, sbls

def flesch_index(stats):
    stcs, words, sbls = stats
    if stcs == 0 or words == 0:
        return 0
    return -1.015 * (words / stcs) + -84.6 * (sbls / words) + 206.835

def flesch_kincaid_level(stats):
    stcs, words, sbls = stats
    if stcs == 0 or words == 0:
        return 0
    return 0.39 * (words / stcs) + 11.8 * (sbls / words) - 15.59

def results(text):
    stats = stcs, words, sbls = text_stats(text)

    # reading ease
    fi = flesch_index(stats)

    # grade level
    fk = flesch_kincaid_level(stats)

    return (fi, fk)
