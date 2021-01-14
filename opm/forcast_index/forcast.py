"""
determine forcast grade level and reading age from a doc object
"""
#from syllapy import count as estimate
from textstat import syllable_count
def forcast(doc):
    """
    :param: doc object
    :returns: tuple with grade level, age level
    """
    word_tokens = doc.word_tokens
    monosyllables = 0

    for i in word_tokens:
        if i.isalpha() == False and len(i) < 2:
            word_tokens.remove(i)
    for i in word_tokens[10:159]:
        if syllable_count(i) < 2:
            monosyllables += 1

    gl = 20 - (monosyllables/10)
    ra = 25 - (monosyllables/10)
    return (gl, ra, monosyllables)
