#!/usr/bin/env python
# -*- coding: utf-8 -*-



import math

from .utils import get_char_count
from .utils import get_words
from .utils import get_sentences
from .utils import count_syllables
from .utils import count_complex_words


class Readability(object):
    analyzedVars = {}

    def __init__(self, text):
        self.analyze_text(text)

    def analyze_text(self, text):
        words = get_words(text)
        char_count = get_char_count(words)
        word_count = len(words)
        sentence_count = len(get_sentences(text))
        syllable_count = count_syllables(words)
        complexwords_count = count_complex_words(text)
        avg_words_p_sentence = word_count/sentence_count

        self.analyzedVars = {
            'words': words,
            'char_cnt': float(char_count),
            'word_cnt': float(word_count),
            'sentence_cnt': float(sentence_count),
            'syllable_cnt': float(syllable_count),
            'complex_word_cnt': float(complexwords_count),
            'avg_words_p_sentence': float(avg_words_p_sentence)
        }
        

    def ARI(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = 4.71 * (self.analyzedVars['char_cnt'] / self.analyzedVars['word_cnt']) + 0.5 * (self.analyzedVars['word_cnt'] / self.analyzedVars['sentence_cnt']) - 21.43
        return score

    def FleschReadingEase(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = 206.835 - (1.015 * (self.analyzedVars['avg_words_p_sentence'])) - (84.6 * (self.analyzedVars['syllable_cnt']/ self.analyzedVars['word_cnt']))
        return round(score, 4)

    def FleschKincaidGradeLevel(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = 0.39 * (self.analyzedVars['avg_words_p_sentence']) + 11.8 * (self.analyzedVars['syllable_cnt']/ self.analyzedVars['word_cnt']) - 15.59
        return round(score, 4)

    def GunningFogIndex(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = 0.4 * ((self.analyzedVars['avg_words_p_sentence']) + (100 * (self.analyzedVars['complex_word_cnt']/self.analyzedVars['word_cnt'])))
        return round(score, 4)

    def SMOGIndex(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = (math.sqrt(self.analyzedVars['complex_word_cnt']*(30/self.analyzedVars['sentence_cnt'])) + 3)
        return score

    def ColemanLiauIndex(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = (5.89*(self.analyzedVars['char_cnt']/self.analyzedVars['word_cnt']))-(30*(self.analyzedVars['sentence_cnt']/self.analyzedVars['word_cnt']))-15.8
        return round(score, 4)

    def LIX(self):
        longwords = 0.0
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            for word in self.analyzedVars['words']:
                if len(word) >= 7:
                    longwords += 1.0
            score = self.analyzedVars['word_cnt'] / self.analyzedVars['sentence_cnt'] + float(100 * longwords) / self.analyzedVars['word_cnt']
        return score

    def RIX(self):
        longwords = 0.0
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            for word in self.analyzedVars['words']:
                if len(word) >= 7:
                    longwords += 1.0
            score = longwords / self.analyzedVars['sentence_cnt']
        return score


#if __name__ == "__main__":
#    text = """
#    I think that student should be able to leave campus for lunch. I believe this because this makes us more responsible and more independent. Also the food at this school is horrible, last year the cheese came off of the so called pizza. This year they same have to same food, revolution. One of my friend forgot there home lunch and when lunch came around she started complaining because she was hungry so I said “well get school lunch.” She said why would I get school lunch and why would I pay 4 dollars for it.
#    So instead of eating the school lunch you can either take the bus or walk to a restaurant. For example you could go to by Takoma station and get food it’s only a like a 20 minutes walk or if you take the 53 or 52 bus it will take 7-10mins. Or you can go to Takoma park and have a picnic and come back to school before class starts.
#    I know there a lot of bad things about this plan. For example (a) student(s) doesn’t come back to school or there late for their class, but that is preparing them for college.
#    """

#    rd = Readability(text)
#    print 'Test text:'
#    print '"%s"\n' % text
#    print 'ARI: ', rd.ARI()
#    print 'FleschReadingEase: ', rd.FleschReadingEase()
#    print 'FleschKincaidGradeLevel: ', rd.FleschKincaidGradeLevel()
#    print 'GunningFogIndex: ', rd.GunningFogIndex()
#    print 'SMOGIndex: ', rd.SMOGIndex()
#    print 'ColemanLiauIndex: ', rd.ColemanLiauIndex()
#    print 'LIX: ', rd.LIX()
#    print 'RIX: ', rd.RIX()
