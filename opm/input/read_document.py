# -*- coding: utf-8 -*-
"""Creates document instance for analysis for semantics and lexical statistics.

Opens and reads document to string raw_text. Relies on textract to handle
.txt, .odt, docx.
"""
from sentence_types.sentence_types import SentenceTypes
#import tika
import codecs
import datetime
import io
import json
import math
import os
import re
import string
import sys
import time
import tokenize as tokeniza
from collections import Counter
from curses.ascii import isdigit
import mimetypes
from random import randint
import docx2txt
import requests
from enchant.checker import SpellChecker
from gensim.summarization import summarize
from langdetect import detect
from pseudolexile.fkToLexile import getLexile
import generate_api_data
import nltk
import readtime
import textract
import unidecode
import wptools
from annotations.markupText import annotateStyle
from annotations.markupText import annotateStructure
from cliches import cliches
from conventions.conventions import main as grammar
from convertDoc.to_body import html_body
from difficult_spelling.difficult_words import difficult_spells
from external import external_calls, sentiment
# from external import web_search
from external.education import education_result
#from external.rosette_auth import rosette_auth
from external.service_informant import Textgain
from ner.ner import ner
from nltk import FreqDist, ne_chunk, pos_tag, tokenize
from nltk.corpus import cmudict, stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer, word_tokenize
from objdict import ObjDict
from passive.passive import main as passive
from plot.plot import bar_h, spline
#from proselint.tools import lint
from readability.readability import Readability
from forcast_index import forcast
from rosette.api import API, DocumentParameters, RosetteException
from sentiment import sentiment
from subject_extraction import subject_extraction
from textblob import TextBlob
#from textgain import textgain
from textgain.textgain import textgain
from textstat.textstat import textstat
from weaselWords.weaselWords import weasels
from linty import lint_text
#from ODTReader.odtreader import odtToText

# try:
#     from external.aylien import auth as aylien_auth
# except:
#
#     pass

#nltk.internals.config_java("/usr/bin/java")
#untested
from distutils.spawn import find_executable
nltk.internals.config_java(find_executable("java"))



class Sample:
    """Represents a document analysis.

    Uses textract to read document into a long string.  The methods are various
    sequences to get information to help make decisions for deliberate academic
    writing.
    """

    def __init__(self, writing, author="anonymous", remote_calls="no"):
        """
        Create document instance for analysis.

        Opens and reads document to string raw_text.
        Textract interprets the document format and
        opens to plain text string (docx, pdf, odt, txt)

        Args:
            path (str): path to file to open, anaylze, close


        Public attributes:
        -user: (str) optional string to set username.
        -path: (str) relative path to document.
        -abs_path: (str) the absolute path to the document.
        -file_name:  (str) the file name with extension of document (base
        name).
        -mime:  tbd
        -guessed_type:  makes best guess of mimetype of document.
        -file_type:  returns index[0] from guessed_type.
        -raw_text:  (str) plain text extracted from .txt, .odt, .pdf, .docx,
        and .doc.
        -ptext:  (str) raw text after a series of regex expressions to
        eliminate special characters.
        -text_no_feed:  (str) ptext with most new line characters eliminated
        /n/n stays intact.
        -sentence_tokens:  list of all sentences in a comma separated list
        derived by nltk.
        -sentence_count:  (int) count of sentences found in list.
        -passive_sentences:  list of passive sentences identified by the
        passive module.
        -passive_sentence_count:  count of the passive_sentences list.
        -percent_passive:  (float) ratio of passive sentences to all sentences
        in percent form.
        -be_verb_analysis:  (int) sum number of occurrences of each to be verb
        (am, is, are, was, were, be, being been).
        -be_verb_count: tbd
        -be_verb_analysis: tbd
        -weak_sentences_all:  (int) sum of be verb analysis.
        -weak_sentences_set:  (set) set of all sentences identified as
        having to be verbs.
        -weak_sentences_count:  (int) count of items in weak_sentences_set.
        -weak_verbs_to_sentences:  (float) proportion of sentences with to
        be to all sentences in percent (this might not be sound).
        -word_tokens:  list of discreet words in text that breaks
        contractions up (default nltk tokenizer).
        -word_tokens_no_punct:  list of all words in text including
        contractions but otherwise no punctuation.
        -no_punct:  (str) full text string without sentence punctuation.
        -word_tokens_no_punct:  uses white-space tokenizer to create a list
        of all words.
        -readability_flesch_re:  (int) Flesch Reading Ease Score (numeric
        score) made by textstat module.
        -readability_smog_index:  (int) grade level as determined by the
        SMOG algorithum made by textstat module.
        -readability_flesch_kincaid_grade:  (int)  Flesch-Kincaid grade level
        of reader made by textstat module.
        -readability_coleman_liau_index:  (int) grade level of reader as made by
        textstat module.
        -readability_ari:  (int) grade leader of reader determined by
        automated readability index algorithum implemented by textstat.
        -readability_linsear_write:  FIX SPELLING grade level as determined
        by Linsear Write algorithum implemented by textstat.
        -readability_dale_chall:  (int) grade level based on Dale-Chall
        readability as determined by textstat.
        -readability_standard:  composite grade level based on readability
        algorithums.
        -flesch_re_key:  list for interpreting Flesch RE Score.
        -word_count:  word count of document based on white space tokener,
        this word count should be used.
        -page_length:  (float) page length in decimal format given 250
        words per page.
        -paper_count:  (int) number of printed pages given 250 words per
        page.
        -parts_of_speech:  words with parts of speech tags.
        -pos_counts:  values in word, tag couple grouped in a list (Counter).
        -pos_total:  (int) sum of pos_counts values
        -pos_freq:  (dict) word, ratio of whole
        -doc_pages:  (float) page length based on 250 words per page
        (warning, this is the second time this attribute is defined).
        -freq_words:  word frequency count not standardized based on the
        correct word tokener (not ratio, just count).
        modal_dist:  count of auxillary verbs based on word_tokens_no_punct.
        sentence_count (int): Count the sentence tokens
        passive_sentences (list): List of all sentences identified as passive
        passive_sentence_count (int): count of items in passive_sentences
        be_verb_count (int): count "to be" verbs in text
        word_tokens_no_punct (list): words separated, stripped of punctuation,
         made lower case
        flesch_re_key (str): reading ease score to description
        freq_words (list or dict): frequency distribution of all words
        modal_dist (list): frequency distribution of aux verbs
        """
        """TIME the Process"""
        self.start = time.time()
        if remote_calls == "yes":
            self.requests_enabled = True
        else:
            self.requests_enabled = False
        #author
        self.author = author

        if len(self.author.split(" ")) > 1:
            self.author_full = self.author
            self.author_first_name = self.name_split(self.author_full)[0]
            self.author_last_name = self.name_split(self.author_full)[1]
        # todo:: user
        self.user = ""
        self.administrator = ""
        self.admin_notes = ""
        self.description = ""


        if os.path.isfile(writing):
            self.abs_path = os.path.abspath(writing)
            self.file_bytes = os.path.getsize(self.abs_path)
            self.file_kbytes = float(self.file_bytes/1000.0)
            self.file_name = os.path.basename(writing)
            self.file_name_no_ext = self.file_name.split('.')[0]
            self.guessed_type = mimetypes.guess_type(writing)
            self.file_type = self.guessed_type[0]
            #self.raw_text = textract.process(writing,
                #encoding="unicode_internal")
            #self.raw_text = unidecode.unidecode_expect_nonascii(self.raw_text)
            if self.file_type == \
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                print("Processing docx:", self.abs_path)
                #self.raw_text = str(self.docxDeal(self.abs_path))
                #self.raw_text = str(self.docxDeal(self.abs_path), 'utf-8')
                #self.raw_text = self.docxDeal(self.abs_path).decode(encoding='UTF-8')
                self.raw_text = self.docxDeal(self.abs_path)
                print(type(self.raw_text))
            elif self.file_type == \
                        "application/vnd.oasis.opendocument.text":
                #self.raw_text = str(self.odtDeal(self.abs_path):
                #self.raw_text = str(self.odtDeal(self.abs_path), 'utf-8')
                self.raw_text = textract.process(self.abs_path)
            elif self.file_type == "text/plain":
                #self.raw_text = io.open(self.abs_path, mode='r', encoding='utf-8')
                #self.raw_text = self.raw_text.read()
                #print(type(self.raw_text))
                #self.raw_text = codecs.open(self.abs_path, encoding='utf-8', mode='r')
                #self.raw_text = self.raw_text.read()
                #print(type(self.raw_text))
                #self.raw_text = unicode(self.raw_text)


                # THIS ONE WORKS for just a str
                self.raw_text = tokeniza.open(writing).read()
                #self.raw_text = str(tokeniza.open(self.abs_path).read(), 'utf-8') # be ready to undo this
                #self.raw_text = open(self.abs_path, encoding="ascii", errors="surrogateescape").read()
                # try:
                #     self.raw_text = unidecode.unidecode_expect_nonascii(self.raw_text)
                # except:
                #     pass
                #self.raw_text = self.raw_text
            elif self.file_type == "application/pdf":
                #self.raw_text = tika.parser.from_file(self.abs_path)
                #self.raw_text = str(textract.process(writing), 'utf-8')
                self.raw_text = textract.process(self.abs_path)
            elif self.file_type == "application/msword":
                #self.raw_text = str(textract.process(writing), 'latin1')
                self.raw_text = textract.process(self.abs_path)
            else:
                self.raw_text = textract.process(writing)
                #self.raw_text = unidecode.unidecode_expect_nonascii(self.raw_text)
                #self.raw_text = self.raw_text
        else:
            self.raw_text = writing
        #         else:
        #             #self.raw_text = unidecode.unidecode_expect_nonascii(writing)
        #             self.raw_text = str(writing, 'utf-8')
        #     except:
        #         pass
        #as long as there's text
            #while "  " in self.raw_text:
            #    self.raw_text = self.raw_text.replace("  ", " ")
            #print(type(self.raw_text))
        if self.raw_text:
            if type(self.raw_text) == str:
                pass
            else:
                self.raw_text = self.raw_text.decode('utf-8')
                print(type(self.raw_text))


            #elif type(self.raw_text) == 'str':
             #   self.raw_text = byte(self.raw_text).replace("  ", " ") # indent to return to previous state



            self.text_language = detect(self.raw_text) # stops processing from peer.py
            self.time_stamp = self.timestamp()
            #self.ptext = re.sub(u'[\u201c\u201d]', '"', self.raw_text)
            #self.ptext = re.sub(u"\u2014", "--", self.ptext)
            #self.ptext = re.sub(",", ",", self.ptext)
            #self.ptext = re.sub("—", "--", self.ptext)
            #self.ptext = re.sub("…", "...", self.ptext)

            print("Cleaning double spaces")
            while "  " in self.raw_text:
                self.raw_text = self.raw_text.replace("  ", " ")
            self.word_tokens = self.word_tokenize(self.raw_text)
            self.text_no_feed = self.clean_new_lines(str(self.raw_text)) # to be deleted
            self.sentence_tokens = self.sentence_tokenize(str(self.raw_text))
            self.sentence_count = len(self.sentence_tokens)
            self.passive_sentences = passive(str(self.raw_text))
            self.passive_sentence_count = len(self.passive_sentences)
            self.percent_passive = (100 *
                                        (float(self.passive_sentence_count) /
                                            float(self.sentence_count)))
            self.percent_passive_round = round(self.percent_passive, 2)
            self.hard_spelling = difficult_spells(str(self.raw_text))
            self.be_verb_analysis = self.count_be_verbs(self.sentence_tokens)
            self.be_verb_count = self.be_verb_analysis[0]
            self.be_verb_tally = self.be_verb_counting(self.word_tokens)

            self.weak_sentences_all = self.be_verb_analysis[1]
            self.weak_sentences_set = set(self.weak_sentences_all)
            self.weak_sentences_count = len(self.weak_sentences_set)
            self.percent_weak_sentence_round = round(100*(float(self.weak_sentences_count)/float(len(self.sentence_tokens))), 2)
            self.weak_verbs_to_sentences = round(float(
                self.be_verb_tally) / float(self.sentence_count), 2)
            self.weak_verbs_to_sentences_round = round(
                self.weak_verbs_to_sentences, 2)


            self.no_punct = self.strip_punctuation(self.raw_text)
            self.word_tokens_no_punct = \
                self.word_tokenize_no_punct(str(self.no_punct))
            # use this! It make lower and strips symbols
            self.word_tokens_no_punct = self.ws_tokenize(self.no_punct)

            #HTML
            self.html = html_body(self.raw_text).decode('utf-8')
            #self.html = self.html.decode('utf-8')




            # readability data

            # self.readability_flesch_re = \
            #     textstat.flesch_reading_ease(str(self.raw_text))
            # #self.readability_smog_index = \
            # #    textstat.smog_index(self.text_no_feed)
            # self.readability_flesch_kincaid_grade = \
            #     textstat.flesch_kincaid_grade(str(self.raw_text))
            # self.readability_coleman_liau_index = \
            #     textstat.coleman_liau_index(str(self.raw_text))
            # self.readability_ari = \
            #     textstat.automated_readability_index(str(self.raw_text))
            #self.readability_gunning = \
            #    textstat.gunning_fog(self.raw_text)
            self.readability_linsear_write = \
                round(textstat.linsear_write_formula(str(self.raw_text)), 2)
            self.readability_dale_chall = \
                textstat.dale_chall_readability_score(str(self.raw_text))
            #self.readability_standard = \
            #    textstat.text_standard(str(self.raw_text))
            self.polysyllabcount = textstat.polysyllabcount(self.raw_text)
            self.lexicon_count = textstat.lexicon_count(str(self.raw_text))
            # Readability Module
            self.readability = Readability(self.raw_text)
            self.readability_ari = round(self.readability.ARI(), 2)
            self.readability_coleman_liau = round(self.readability.ColemanLiauIndex(), 2)
            self.readability_fleschkincaid = round(self.readability.FleschKincaidGradeLevel(), 2)
            self.readability_flesch_re = round(self.readability.FleschReadingEase(),2)
            self.readability_gunningfog = round(self.readability.GunningFogIndex(), 2)

            self.readability_smog = round(self.readability.SMOGIndex(), 2)
            self.readability_lix = round(self.readability.LIX(), 2)
            self.readability_lix_grade = self.lix_grade(self.readability_lix)

            self.readability_forcast = forcast(self)
            # textstat
            self.flesch_re_desc_str = self.flesch_re_desc(round(self.readability_flesch_re, 0))
            try:
                self.readability_standard = self.get_standard()
            except TypeError:
                self.readability_standard = "null"
            ### readability from a different module###
            self.stats = self.readability.analyzedVars
            self.syllable_count = self.stats['syllable_cnt']
            self.complex_word_cnt = self.stats['complex_word_cnt']
            self.avg_words_p_sentence = self.stats['avg_words_p_sentence']
            # self.readability_smog_index = round(self.smog(str(self.raw_text)), 2)
            # self.readability_gunning = round(self.gunning_fog(str(self.raw_text)), 2) # doesn't work
            # self.readability_lix = round(self.lix(str(self.raw_text)), 2) # no result
            # self.readability_rix = round(self.rix(str(self.raw_text)), 2) # no result
            # self.readability_forcast = forcast(self)

            self.lexile = getLexile(self.readability_fleschkincaid)
            # Back to original module
            self.avg_syllables_per_word = textstat.avg_syllables_per_word(
                str(self.raw_text))
            self.avg_sentence_per_word = textstat.avg_sentence_per_word(
                str(self.raw_text))
            self.avg_sentence_length = textstat.avg_sentence_length(
                str(self.raw_text))
            self.avg_letter_per_word = textstat.avg_letter_per_word(
                str(self.raw_text))
            self.long_sentences = self.sentences_20(self.sentence_tokens)
            self.difficult_words = textstat.difficult_words(str(self.raw_text))

            self.word_count = len(self.word_tokens_no_punct)
            self.page_length = float(self.word_count)/float(250)
            self.paper_count = int(math.ceil(self.page_length))
            self.parts_of_speech = pos_tag(self.word_tokens_no_punct)
            self.pos_counts = Counter(tag for word, tag in
                                        self.parts_of_speech)
            self.pos_total = sum(self.pos_counts.values())
            self.pos_freq = dict((word, float(count)/self.pos_total) for
                                    word, count in list(self.pos_counts.items()))
            self.doc_pages = float(float(self.word_count)/float(250))
            self.freq_words = \
                self.word_frequency(self.word_tokens_no_punct)
            self.modal_dist = self.modal_count(self.word_tokens_no_punct)
            # self.ws_tokens = self.ws_tokenize(self.text_no_cr)
            self.pos_count_dict = list(self.pos_counts.items())
            # model for ony pos count
            self.modals = self.pos_isolate(
                'MD', self.pos_count_dict)
            self.preposition_count = self.pos_isolate(
                            'IN', self.pos_count_dict)
            self.adjective_count = self.pos_isolate_fuzzy(
                'JJ', self.pos_count_dict)
            self.adverb_count = self.pos_isolate_fuzzy(
                'RB', self.pos_count_dict)
            self.proper_nouns = self.pos_isolate_fuzzy(
                'NNP', self.pos_count_dict)
            self.cc_count = self.pos_isolate('CC', self.pos_count_dict)
            # verb_tense: make function
            self.tense = {}
            self.tense['future'] = self.pos_counts['VBC'] +     self.pos_counts['VBZ']
            self.tense['present'] = self.pos_counts['VBP'] +     self.pos_counts['VBZ'] + self.pos_counts['VBG']
            self.tense['past'] = self.pos_counts['VBD'] +     self.pos_counts['VBN']
            self.overall_tense = self.weigh_tense(self.tense)



            # commas
            self.commas = self.char_count(",")
            self.comma_sentences = self.list_sentences(",")
            if self.comma_sentences:
                self.comma_example = self.select_random(len(self.comma_sentences), self.comma_sentences)
            # semicolons
            self.semicolons = self.char_count(";")
            self.semicolon_sentences = self.list_sentences(";")
            if self.semicolon_sentences:
                self.semicolon_example = self.select_random(len(self.semicolon_sentences), self.comma_sentences)
            if self.semicolon_sentences:
                if len(self.semicolon_sentences) > 3:
                    self.semicolon_example = self.select_random(len
                                                            (self.semicolon_sentences),
                                                self.semicolon_sentences)
                else:
                    self.semicolon_example = self.semicolon_sentences[0]
            #readtime
            self.toRead = self.time_to_read()
            # Adverbs
            if self.adjective_count > 0:
                try:
                    self.adverb_to_adjective = round(float(self.adverb_count)/float(self.adjective_count), 3)
                except:
                    self.adverb_to_adjective = "Calculation Error"
            # exclamations
            #self.bangs = self.char_count("!")
            self.exclamations = self.list_sentences("!")
            self.exclamation_count = len(self.exclamations)
            # very
            self.very_count = self.word_check('very')
            #proselint
            self.lint_suggestions = lint_text(self.raw_text)
            # if self.lint_suggestions:
            #     self.lint_list = self.lint_extractor(self.lint_suggestions)
            # else:
            #     self.lint_list = ""
            # unrecognized words
            self.unrecognized_words = self.spelling(str(self.raw_text))
            #self.unrecognized_words = set(self.unrecognized_words)
            for w in self.unrecognized_words:
                if w not in self.word_tokens:
                    self.unrecognized_words.remove(w)
            self.unrecognized_words_count = len(self.unrecognized_words)
            self.unrecognized_words_random = self.select_random(
                    self.unrecognized_words_count,self.unrecognized_words)
            #entities
            self.extracted_names = self.extract_names(str(self.raw_text))
            self.extracted_entities = ner(str(self.raw_text)) #produces list
            self.extracted_entities = set(self.extracted_entities)
            self.named_entity_set = self.combine_entities(self.extracted_names, self.extracted_entities)
            for word in self.unrecognized_words:
                if word in self.named_entity_set:
                    self.unrecognized_words.remove(word)
                    self.unrecognized_words_count -= 1
            #self.names_links = self.get_urls(self.named_entity_set)
            #subject
            try:
                self.subject = subject_extraction.get_subject(str(self.raw_text))
            except:
                self.subject = "Subject could not be identified."
            #cliche catcher
            self.cliche_list = cliches.cliches()
            self.cliche_results = cliches.process_cliches(self.cliche_list,
                                                str(self.raw_text).lower())
            self.cliches_in_text = self.cliche_results[1]
            self.cliche_count = self.cliche_results[0]
            # if external requests
            if self.requests_enabled == True:
                #get urls for named entities
                self.names_links = self.get_urls(self.named_entity_set) #entity links
                #sentiment - external via api
                try:
                    self.api_sentiment = sentiment.sentiment_result(str(self.raw_text))
                except:
                    self.api_sentiment = ""
                    pass

                try:
                    self.concepts = textgain('concepts', str(self.raw_text))
                except:
                    pass
                try:
                    self.edu = textgain('education', str(self.raw_text), language='en')
                except:
                    pass
                # age level (external - call to textgain)
                try:
                    self.age = textgain('age', str(self.raw_text), language='en')
                except:
                    pass
                # guessed gender (external - calls to textgain)
                try:
                    self.gender = textgain('gender', str(self.raw_text))
                except:
                    pass
                #genre (external - calls to textgain)
                try:
                    self.genre = textgain('genre', str(self.raw_text))
                except:
                    pass
                # textgain concepts
                try:
                    self.textgain_concepts = textgain('concepts', str(self.raw_text))
                except:
                    pass
                #personality (external call to textgain)
                try:
                    self.personality = textgain('personality', str(self.raw_text))
                    if self.personality == 'E':
                        self.personality = 'Extrovert'
                    elif self.personality == 'I':
                        self.personality = 'Introvert'
                    else:
                        pass
                except:
                    pass
                #TextProcessing
                self.entities = external_calls.entities(self.raw_text)
                #Rosette
                #try:
                #    self.rosette_client = rosette_auth()
                #    self.rosette_params = DocumentParameters()
                #    self.rosette_params["language"] = "eng"
                #    self.rosette_params.load_document_string(self.raw_text)
                #    self.rosette_sentiment = self.rosette_api.sentiment(self.result)
                #    self.rosette_sentiment_result = self.rosette_sentiment['document']
                #except:
                #    print("Could not contact Rosette dependencies.")
                #    pass
                # Aylien
                """ try:
                    self.aylien_client = aylien_auth()
                    self.combined_aylien = self.aylien_client.Combined({'text': self.raw_text, 'endpoint':["hashtags", "concepts", "classify", "entities"]})
                    self.summary_aylien = self.aylien_client.Summarize({'text': self.raw_text, 'title': self.file_name, 'sentence_number':4})
                    self.summary_paragraph_aylien = " ".join(self.summary_aylien['sentences'])
                    self.hashtags_aylien = self.aylien_client.Hashtags({'text': self.raw_text})
                    self.hashtags =                      self.hashtag_cleaner(self.hashtags_aylien['hashtags']) """
                    #self.entities_aylien = self.aylien_client.Entities({'text':self.raw_text})
                    #self.keywords_aylien = self.entities_aylien['entities']['keyword']

                """ except:

                    pass """

            # TextBlob attributes
            blob = TextBlob(str(self.raw_text))
            self.polarity = round(blob.sentiment.polarity, 3)
            #self.polarity_human = round(self.polarity, 3)
            self.subjectivity = round(blob.sentiment.subjectivity, 3)
            #self.subjectivity_human = round(self.subjectivity, 3)
            # unity
            self.intro = self.sentence_tokens[0]
            self.exit = self.sentence_tokens[-1]

            # noun phrases
            self.phrases = self.tag_phrases(TextBlob(str(self.raw_text)))
            #compound semicolon_sentences
            self.compound_sentences = self.find_compound_sentences(self.sentence_tokens)
            self.compound_sentence_count = len(self.compound_sentences)
            #language_check
            self.check = grammar(str(self.raw_text))
            self.grammar_error_count = self.check[0]
            self.grammar_feedback = self.check[1]
            self.grammar_notes = []
            for f in self.grammar_feedback:
                if "Miscellaneous" not in f.category:
                    self.grammar_notes.append((f.category.upper(), f.context, f.msg, f.replacements))
            self.grammar_messages = self.sanitize_grammar_feedback(self.grammar_feedback)
            self.grammar_message_count = len(self.grammar_messages)
            # pov
            self.grammar_message_list = list(self.grammar_messages)
            self.first_person = self.pronouns(['I', 'me', 'mine', 'myself', 'I\'ve', 'I\'m'], str(self.raw_text))
            self.first_person_count = len(self.first_person)
            self.second_person = self.pronouns([' you ', ' you\'re ', ' yours ', ' your ', ' yourself ', ' you\'ve' ], str(self.raw_text))
            self.second_person_count = len(self.second_person)
            try:
                self.summary = summarize(str(self.raw_text), ratio=0.1, word_count=150)
            except ValueError:
                self.summary = ("Summary could not be provided: Text is only %d words long" % len(self.word_tokens_no_punct))
            self.weasel_words = weasels(str(self.raw_text))
            self.weasel_word_count = len(self.weasel_words)
            self.longest_word = max(str(self.raw_text).split(), key=len)
            self.longest_word_character_count = len(self.longest_word)
            self.longest_sentence_char_count = max(self.sentence_tokens, key=len)
            # returns [[list of words], count]
            self.tion_word_list = self.tion_words(self.word_tokens)
            self.other_modals = self.pos_isolate('MD', self.pos_count_dict)
            self.gerund_count = self.pos_isolate('VBG', self.pos_count_dict)
            self.unique_words = len( set(self.word_tokens_no_punct))
            self.very_long_sentences = self.sentences_30(self.sentence_tokens)
            self.top20words =        self.get_filtered_word_freq(self.word_tokens_no_punct)
            self.unrecognized_words = set(self.unrecognized_words)
            # Sentence Structures
            self.sentenceStructures = SentenceTypes(str(self.raw_text))
            self.transitionSents = self.sentenceStructures.transSentences
            self.complexSents = self.sentenceStructures.complex_sents
            self.compoundSents = self.sentenceStructures.compound_sents
            self.listSents = self.sentenceStructures.list_sents
            self.compComplexSents = self.sentenceStructures.compound_complex_sents
            self.apposSents = self.sentenceStructures.appositive_sents
            self.problemSents = self.sentenceStructures.problem_sents
            self.coordProblems = self.sentenceStructures.coord_start_sents
            self.gerundSents = self.sentenceStructures.gerund_sents

            #self.word_syllables = self.syllables_per_word(self.word_tokens_no_punct)
            #Web Searches
            # web Results
            if self.requests_enabled == True:

                try:
                    self.longest_word_abstract = web_search.definition(self.longest_word)

                    #self.close_matches = web_search.google_search(str(self.raw_text))
                except:
                    pass



            #### For cheap evaluation report ####
            # proportion unique words to all words
            self.percent_unique = round((self.unique_words / self.word_count) * 100, 2)

            # nominalization (sort of)
            self.percent_nominalization = round((((self.tion_word_list[1] + self.gerund_count) / 2) / self.word_count) * 100,2)
            # average of total percent and total weak as percent of all sentences
            self.percent_lardy = round(((((self.percent_passive_round + self.percent_weak_sentence_round) / 2)/ self.sentence_count) * 100), 2)
            # Prepositions per sentence rounded
            self.prepositions_per_sentence = round(self.preposition_count/self.sentence_count, 2)
            # percent complex words
            self.percent_complex = round((self.complex_word_cnt/self.word_count)*100, 2)
            # percent modal of all words
            self.percent_modal = round(((self.modals / self.word_count) * 100),2)
            self.analysis = {'readability standard':self.readability_standard,
                'reading difficulty':self.flesch_re_desc_str,
                'percent unique': self.percent_unique,
                'percent nominalized': self.percent_nominalization,
                'percent lardy': self.percent_lardy,
                'subject': self.subject,
                'top word': self.top20words[0][0],
                'intro': self.intro,
                'conclusion': self.exit,
                'adverbs to adjectives': round(self.adverb_to_adjective, 2),
                'percent complex words': round(self.percent_complex, 2),
                'percent modal': round(self.percent_modal,2),
                'percent polysyllable': round((self.polysyllabcount/self.word_count) * 100, 2)
                }

            # Generate JSON representation

            #self.api_report = ObjDict()

            #self.api_report.identification = self.file_name + " " + self.time_stamp,
            #self.api_report.summary = self.summary
            """self.api_report.statistics = {
                "Word Count": self.lexicon_count,
                "Page Count": self.page_length,
                "Polysyllables": self.polysyllabcount,
                "Average Sentence Length": self.avg_sentence_length
                }
            self.api_report.readability = {
                "Readability Standard": self.readability_standard,
                "Reading Difficulty": self.flesch_re_desc_str
                }"""

            self.sentiment_score = self.sentiment_vader(str(self.raw_text))
            #questions
            self.question_marks = self.char_count("?")
            self.questions = self.list_sentences("?")
            try:
                if len(self.questions) >= 4:
                    self.question_example = self.select_random(len(self.questions), self.questions)
                elif len(self.questions) > 0:
                    self.question_example = self.questions[0]
                else:
                    self.question_example = "None available."
            except:
                self.question_example = "None available."
            # passive and weak
            if self.passive_sentence_count:
                self.rand_passive = self.select_random(self.passive_sentence_count,
                                                    self.passive_sentences)
            if len(self.weak_sentences):
                self.rand_weak_sentence = self.select_random(
                len(self.weak_sentences), self.weak_sentences)
            if len(self.exclamations) > 2:
                self.exclamation_example = self.select_random(self.exclamation_count, self.exclamations)
            elif self.exclamations:
                self.exclamation_example = self.exclamations[0]
            '''self.api_report.concision = {
                    "'To Be' Verb Count": self.be_verb_count,
                    "To Be Proportion": self.weak_verbs_to_sentences_round,
                    "Other Modals": self.modals,
                    "Percent Passive": self.percent_passive_round,
                    "Weak Verb Example": self.rand_weak_sentence,
                    "Passive Example": self.rand_passive,
                    "'-tion words'": len(self.tion_word_list),
                    "Gerunds": self.gerund_count
                }'''
            #self.end = time.time() - self.start #duplicate
            self.sentiment_plot = self.plot_sent(self.sentence_tokens)
            self.plot_subj =  self.plot_subjectivity(self.sentence_tokens)
            self.plot_read = self.plot_readability_scores(self.readability_standard)

            self.sentence_tense_list = self.get_sentence_tenses(self.sentence_tokens)
            #self.markedupText = self.markupText()
            self.annotatedText = annotateStyle(self)
            self.annotatedStructure = annotateStructure(self)
            self.end = time.time() - self.start
            print(("Time to Process Submission: %s" % self.end))

    def get_sentence_tenses(self, sentence_tokens):
        sentence_tense = []
        for sentence in sentence_tokens:
            sentence_tense.append((sentence, self.determine_tense_input(sentence)))
        return sentence_tense

    def determine_tense_input(self,sentence):
        text = word_tokenize(sentence)
        tagged = pos_tag(text)
        tense = {}
        tense["future"] = len([word for word in tagged if word[1] in ["VBC", "VBF"]])
        tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
        tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
        return self.weigh_tense(tense)


    def weigh_tense(self, source):
        if source['present'] > source['past'] and source['present'] > source['future']:
            return 'present'
        elif source['past'] > source['present'] and source['past'] > source['future']:
            return 'past'
        elif source['future'] > source['present'] and source['future'] > source['past']:
            return 'future'
        else:
            return 'not available'

    def flesch_re_desc(self, score):
        if score < 30:
            return "Very Confusing"
        elif score < 50 and score > 29:
            return "Difficult"
        elif score < 60 and score > 49:
            return "Fairly Difficult"
        elif score > 59 and score < 70:
            return "Standard"
        elif score > 69 and score < 80:
            return "Fairly Easy"
        elif score < 90 and score > 79:
            return "Easy"
        else:
            return "Very Easy"
    def lix_grade(self, score):
        if score < 10.0:
            return 1
        elif score < 15:
            return 2
        elif score < 20:
            return 3
        elif score < 24:
            return 4
        elif score < 28:
            return 5
        elif score < 32:
            return 6
        elif score < 36:
            return 7
        elif score < 40:
            return 8
        elif score < 44:
            return 9
        elif score < 48:
            return 10
        elif score < 52:
            return 11
        elif score <= 55:
            return 12
        else:
            return "college"
    # heavily influenced or lifted from textstat at https://github.com/shivam5992/textstat
    def legacy_round(self, number, points=0):
        p = 10 ** points
        number = float(number)
        return float(math.floor((number * p) + math.copysign(0.5, number))) / p
    def get_grade_suffix(self, grade):
        """
        Select correct ordinal suffix
        """
        ordinal_map = {1: 'st', 2: 'nd', 3: 'rd'}
        teens_map = {11: 'th', 12: 'th', 13: 'th'}
        return teens_map.get(grade % 100, ordinal_map.get(grade % 10, 'th'))
    def get_standard(self):
        try:
            grade = [int(self.legacy_round(self.readability_ari)), \
                int(math.ceil(self.readability_ari)), \
                int(self.legacy_round(self.readability_coleman_liau)), \
                int(math.ceil(self.readability_coleman_liau)), \
                int(self.legacy_round(self.readability_dale_chall)), \
                int(math.ceil(self.readability_dale_chall)), \
                int(self.legacy_round(self.readability_fleschkincaid)), \
                int(math.ceil(self.readability_fleschkincaid)), \
                int(self.legacy_round(self.readability_forcast[0])), \
                int(math.ceil(self.readability_forcast[0])), \
                int(self.legacy_round(self.readability_gunningfog)), \
                int(math.ceil(self.readability_gunningfog)), \
                int(self.legacy_round(self.readability_linsear_write)), \
                int(math.ceil(self.readability_linsear_write)), \
                int(self.legacy_round(self.readability_lix_grade)), \
                int(math.ceil(self.readability_lix_grade)), \
                int(self.legacy_round(self.readability_smog)), \
                int(math.ceil(self.readability_smog))]
        except ValueError:
            grade = [int(self.legacy_round(self.readability_ari)), \
                int(math.ceil(self.readability_ari)), \
                int(self.legacy_round(self.readability_coleman_liau)), \
                int(math.ceil(self.readability_coleman_liau)), \
                int(self.legacy_round(self.readability_dale_chall)), \
                int(math.ceil(self.readability_dale_chall)), \
                int(self.legacy_round(self.readability_fleschkincaid)), \
                int(math.ceil(self.readability_fleschkincaid)), \
                int(self.legacy_round(self.readability_forcast[0])), \
                int(math.ceil(self.readability_forcast[0])), \
                int(self.legacy_round(self.readability_gunningfog)), \
                int(math.ceil(self.readability_gunningfog)), \
                int(self.legacy_round(self.readability_linsear_write)), \
                int(math.ceil(self.readability_linsear_write)), \
                int(self.legacy_round(self.readability_smog)), \
                int(math.ceil(self.readability_smog))]
        d = Counter(grade)
        final_grade = d.most_common(1)

        score = final_grade[0][0]
        lower_score = int(score - 1)
        upper_score = lower_score + 1

        return "{}{} and {}{} grade".format(
                lower_score, self.get_grade_suffix(lower_score),
                upper_score, self.get_grade_suffix(upper_score)
            )

    def strip_punctuation(self, string_in):
        """
        Strip punctuation from string and make it lower case.

        Given a string of sentences, translate string
        to remove *some* common symbols and convert capital
        letters to lower case.

        Args:
            string_in (str): Text to strip punctuation from

        return:
            str
        """
        string_in = str(string_in).translate(',.!?\"<>{}[]--@()\'--')
        return str(string_in.lower())

    def ws_tokenize(self, text):
        """
        Given string of words, return word tokens with  contractions OK.

        Other tokenizers tokenize punctuation. The WhitespaceTokenizer
        is important because of contractions.

        Args:
            text (str)

        returns:
            list

        """
        self.tokenizer = nltk.tokenize.regexp.WhitespaceTokenizer()
        return self.tokenizer.tokenize(text)

    def syllables_per_word(self, list):
        """
        Return count of syllables per word.

        Loops through all words to add word and syllable
        count to a list.

        Args:
        text (str)

        Returns:
        list
        """
        word_syllables = []
        for word in list:
            word_syllables.append((word,
                                        textstat.syllable_count(
                                            word)))
        return word_syllables
    def find_compound_sentences(self, sentences):
        compounds = []
        for s in sentences:
            for c in [', and', ', for', ', nor',  ', but', ', or' ,  ', yet', ', so']:
                if c in s:
                    compounds.append(s)
        return compounds
    def polysyllables(self, text):
        """
        Count polysyllables.

        Count words in text string that have >= 3 syllables.

        Args:
        text(str)

        Returns:
        int: polysllable word count in text arg

        """
        return textstat.textstat.polysyllabcount(text)

    def word_frequency(self, words):
        """
        List 20 most common words in tokenized list.

        memo: words = [word for word in words if not word.isnumeric()].

        Args:
        text(str)

        Returns:
        list
        """
        words = [word.lower() for word in words]
        self.word_dist = FreqDist(words)
        return self.word_dist.most_common(20)

    def word_tokenize_no_punct(self, text):
        """
        Make list of words without listing punctuation.

        Args:
            text (str): Plain text string

        Returns:
             list of words
        """
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(text)

    def word_tokenize(self, paragraph):
        """
        Tokenize words from long string that includes sentences.

        Uses default tokenizer from nltk.

        Args:
            paragraph (str)

        Return:
            list

        """
        try:
            self.word_tokens = tokenize.word_tokenize(paragraph)
            return self.word_tokens
        except:
            print("Error: Cannot perform word analyses.")
            return False

    def sentence_tokenize(self, paragraphs):
        """
        Tokenize sentences.

        Uses default sent tokenizer.

        Args:
        paragraph (str)

        Returns:
        list

        """
        try:
            self.sentences = tokenize.sent_tokenize(paragraphs)
            return self.sentences
        except:
            print("Could not tokenize text.")
            pass

    def clean_new_lines(self, paragraphs):
        """Strip new line characters except for new paragraphs."""
        self.text_no_cr =\
            paragraphs.replace("\n\n",
                           "TOADIES").replace("\r",
                                              "  ").replace("\n",
                                                          "  ").replace(
                                                              "TOADIES", "\n")
        return self.text_no_cr

    def count_be_verbs(self, sentences):
        """
        Count be verbs in each sentence in a list.

        Loop through sentences to provide weak verb count.
        If count >= 1, add sentence to list.

        Args:
            sentences (str, list)

        Return:
            list of be-verb count and stand-out sentences

        """
        self.verbs = ["it's", " am ", " is ", " are ", " was ", " were ", " be ",\
            "being ", " been "]
        self.weak_sentences = []
        self.verb_count = 0
        for sentence in sentences:
            for verb in self.verbs:
                if verb in sentence:
                    self.verb_count = self.verb_count + 1
                    self.weak_sentences.append(sentence)

        return [self.verb_count, self.weak_sentences]

    def be_verb_counting(self, word_bag):
        count = 0
        verbs = ['am', 'is', 'are', 'was', 'were', 'be', 'being', 'been']
        for verb in verbs:
            count += word_bag.count(verb)
        return count

    def syllable_count(self, word):
        """
        Count syllables in a word.

        Uses NLTK dictionary to find word syllabication.

        Args:
            word (string)

        Returns:
            int syllable count

        """
        self.d = cmudict.dict()
        return min([len([y for y in x if isdigit(y[-1])])
                    for x in self.d[str(word).lower()]])

    def modal_count(self, text):
        """
        Return FreqDist of modal verbs in text.

        Args:
            text (str)

        Return:
            list
        """
        fdist = FreqDist(w.lower() for w in text)
        modals = ['can', 'could', 'shall', 'should', 'will', 'would', 'do',
                  'does', 'did', 'may', 'might', 'must', 'has', 'have', 'had']
        modals_freq = []
        for m in modals:
            modals_freq.append(str(m + ': ' + str(fdist[m])))
        return modals_freq

    def timestamp(self, fmt='%Y-%m-%d %H:%M'):
        """
        Set the date and time a document was uploaded.

        Record the datetime a document is uploaded or
        a paste is submitted.

        returns:
           Data and Time in US format, separated by space.
        """
        return datetime.datetime.now().strftime(fmt)

    def select_random(self, count, content):
        """
        Choose a random example from a list.

        Given a list and the length of the list,
        return a random list member.
        """
        #time.sleep(3)
        try:
            if count > 1:
                top_of_range = 0 + count
                choose = randint(0, top_of_range-1)
                return content[choose]
        except:
            print(("Failed to select a random example from  %s. Please try again." % content))
            pass
    def pos_count(self, pos, resource):
        for x,y in resource:
            if x == pos:
                return y

    def pos_isolate(self, pos, dictionary):
        for x, y in dictionary:
            if x == pos:
                return y

    def pos_isolate_fuzzy(self, pos, dictionary):
        for x, y in dictionary:
            if pos in x:
                return y

    def char_count(self, character):
        count = 0
        for sentence in self.sentence_tokens:
            if character in sentence:
                count = count + 1
        return count

    def list_sentences(self, character):
        sentences = []
        for sentence in self.sentence_tokens:
            if character in sentence:
                sentences.append(sentence)
        return sentences

    def spelling(self, text_string):
        chkr = SpellChecker("en_US", text_string)
        unrecognized = []
        for err in chkr:
            if err.word not in unrecognized:
                unrecognized.append(err.word)
        return unrecognized

    def docxDeal(self, file):
        raw_text = docx2txt.process(self.abs_path)
        raw_text = unidecode.unidecode_expect_nonascii(raw_text)
        return raw_text
    def odtDeal(self, file):
        raw_text = textract.process(file, encoding='UTF-8')
        #raw_text = unidecode.unidecode_expect_nonascii(raw_text)
        return raw_text

    #def odtDeal(self, file):
    #    raw_text = odtToText(file)
    #    raw_text = unidecode.unidecode_expect_nonascii(raw_text)
    #    return raw_text
    def sentences_20(self, sentences):
        count = 0
        for sentence in sentences:
            if len(sentence.split()) > 20:
                count += 1
        return count

    def sentences_30(self, sentences):
        count = 0
        for sentence in sentences:
            if len(sentence.split()) > 30:
                   count += 1
        return count

    def tag_phrases(self, blob):
        blob_noun_phrases = blob.noun_phrases
        noun_phrases = []
        for phrase in blob_noun_phrases:
            if phrase not in noun_phrases:
                noun_phrases.append(phrase)
        return noun_phrases

    def pronouns(self, list, words):
        pronouns = []
        for pronoun in list:
            if pronoun in words:
                pronouns.append(pronoun)
        return pronouns

    def hashtag_cleaner(self, hashtags):
        tags = []
        for tag in hashtags:
            tag = tag.replace("#", "")
            tags.append(tag)
        return tags

    def smog(self, txt):
        r = Readability(txt)
        r = r.SMOGIndex()
        return r

    def gunning_fog(self, txt):
        r = Readability(txt)
        r = r.GunningFogIndex()
        return r

    def lix(self, txt):
        r = Readability(txt)
        r = r.LIX()
        return r

    def rix(self, txt):
        r = Readability(txt)
        r = r.RIX()
        return r

    def tion_words(self, string_list):
        results = [[],0]
        for word in string_list:
            if "tion" in word:
                results[0].append(word)
                results[1] += 1
        return results

    def sanitize_grammar_feedback(self, grammar_messages):
        clean_grammar_messages = []
        for item in grammar_messages:
            if "quote" not in item.msg:
                clean_grammar_messages.append(item.msg)
        msg = set(clean_grammar_messages)
        return msg



    def get_filtered_word_freq(self, tokens):
        stopwords = nltk.corpus.stopwords.words('english')
        tokenized_text_no_stopwords = [word for word in tokens if word not in stopwords]
        filtered_word_freq = nltk.FreqDist(tokenized_text_no_stopwords)
        top10words = filtered_word_freq.most_common(20)
        return top10words

    #def __del__(self):
    #    self.__del__()
    #    print("Instance of Class 'Sample' removed.")

    def toJSON(self):
        return json.dumps(self.api_report, sort_keys=False, indent=4)

    def sentiment_vader(self, text):
        ss = SentimentIntensityAnalyzer().polarity_scores(text)
        return ss['compound']

    def name_split(self, name):

        if ", " in name:
            name = name.title()
            name = name.split(", ")

            return name[0], name[1]
        elif " " in name:
            name = name.title()
            name = name.split(" ")
            return name[0], name[1]

        else:
            return None

    def extract_names(self, plaintext):
        from nltk.corpus import stopwords
        stop = stopwords.words('english')
        document = ' '.join([i for i in plaintext.split() if i not in stop])
        sentences = nltk.sent_tokenize(document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        names = []
        for tagged_sentence in sentences:
            for chunk in nltk.ne_chunk(tagged_sentence):
                if type(chunk) == nltk.tree.Tree:
                    if chunk.label() == 'PERSON':
                        names.append(' '.join([c[0] for c in chunk]))
        return names

    def get_urls(self, names):
        names_links = []
        for name in names:
            try:
                link = wptools.page(name).get_query()
                link = link.data['wikidata_url']
                names_links.append([name, link])

            except:
                pass
            #if names_links:
        return names_links

    def plot_sent(self, sentences):
        sents = []
        for s in sentences:
            sents.append(self.sentiment_vader(s))
        return spline(sents, sentences, "Sentiment")
    # Delete
    def plot_subjectivity(self, sentences):
        subjlist = []
        for s in sentences:
            b = TextBlob(s)
            subj = b.sentiment.subjectivity
            subjlist.append(subj)
        return spline(subjlist, sentences, "Subjectivity")
    def plot_readability_scores(self, std):
        index_names = ['ARI', 'Coleman-Liau', 'Dale-Chall', 'Forcast','Flesch-Kincaid', 'Gunnning Fog', 'Linsear Write', 'SMOG Index']

        scores = [self.readability_ari, self.readability_coleman_liau, self.readability_dale_chall, self.readability_forcast[0], self.readability_fleschkincaid, self.readability_gunningfog, self.readability_linsear_write, self.readability_smog]
        div = bar_h(index_names, scores)
        return div
    def lint_extractor(self, list):
        lint_list = []
        for lint in list:
            if "fancy" not in lint[1] and "ellipsis" not in lint[1] and "curly" not in lint[1]:
                lint_list.append(lint[1])
        return lint_list

    def combine_entities(self, python_results, java_results):
        for item in java_results:
            if item[1] == 'LOCATION':
                python_results.append(item[0])
            elif item[1] == 'PERSON':
                python_results.append(item[0])
            elif item[1] == 'ORGANIZATION':
                python_results.append(item[0])
            else:
                pass
        return set(python_results)

    # def toHTML(self, src):
    #     body = html_body(Doc.raw_text)
    #     return

    def toDict(self):
        self.serialized = ObjDict()
        self.serialized.identity = self.time_stamp
        #self.serialized.summary = self.summary
        self.serialized.statistics = {
             "wordCount":self.word_count, "sentenceCount":self.sentence_count,
             "longSentences":self.long_sentences, "veryLongSentences":self.very_long_sentences, "avgSentLength":self.avg_sentence_length,
             "polysyllables":self.polysyllabcount, "avgSyllablesPerword":self.avg_syllables_per_word,
             "difficultWords": self.difficult_words
        }
        self.serialized.readability = {
            "readabilityStandard":self.readability_standard, "readingDifficulty":self.flesch_re_desc_str,
            "indexes": {
                "fleschKincaid":self.readability_flesch_kincaid_grade,
                "ARI":self.readability_ari,
                "colemanLiau": self.readability_coleman_liau_index,
                "smog":self.readability_smog_index,
                "chall":self.readability_dale_chall,
                "linsear":self.readability_linsear_write,
                "gunningFog":self.readability_gunning
            }
        },
        self.serialized.concision = {
             "toBeVerbCount":self.be_verb_count, "toBeRatio":self.weak_verbs_to_sentences_round, "otherModals":self.modals,
             "percentPassive":self.percent_passive_round,
             "gerunds":self.gerund_count,
             "prepositions":self.preposition_count,
             "prepositionsPerSentence": self.prepositions_per_sentence
        },
        self.serialized.voice = {
            "firstPerson":self.first_person_count,
            "secondPerson":self.second_person_count,
            "sentiment":self.sentiment_score,
            "subjectivity":self.subjectivity_human,
            "modifiers": {
                "adjectiveCount":self.adjective_count,
                "adverbCount":self.adverb_count
            }
        },
        try:
            self.serialized.examples = {
                "commaSentence":self.comma_example,
                "interroSentence": self.question_example,
                "beSentence": self.rand_weak_sentence,
                "semicolonSentence": self.semicolon_example,
                "exclamSentence": self.exclamation_example,
                "passiveSentence": self.rand_passive
            },
        except:
            pass
        self.serialized.notes = {
            "unrecognizedWords": [self.unrecognized_words],
            "cliches": [self.cliches_in_text],
            "linter": self.lint_list,
            "tionSuffixes": [self.tion_word_list[0]],
            "correctlySpelled": [self.hard_spelling],
            "grammarNotes": [self.grammar_message_list]
        },
        self.serialized.unity = {
            "nounPhrases": [self.phrases],
            "top20words": self.top20words,
            "introduction": self.intro,
            "conclusion":self.exit
        }
        return self.serialized

    def word_check(self, word):
        count = 0
        for w in self.word_tokens:
            if w == word:
                count += 1
        return count
    def time_to_read(self):
        readit = readtime.of_text(str(self.raw_text))
        return readit.text


'''
    def markupText(self):
        document = '<div class="essay"><table class="table table-striped"><tbody>'

        # sentences
        for sent in self.sentence_tokens:
            if sent in self.passive_sentences:
                document += '<tr><td><p class="passive"> %s <span style="font-size:15px" class="pull-right label label-large label-danger">Passive</span></p></td></tr>' % sent
            elif sent in self.weak_sentences:
                document += '<tr><td><p class="weak"> %s <span style="font-size:15px" class="pull-right label label-large label-danger">Weak Verb(s)</span></p></td></tr>' % sent
            else:
                document += "<tr><td><p> %s </p></td></tr>" % sent

        # words and phrases
        document = document.replace("But", '<span class="but" style="border:2px #d9534f solid" title="Start with But only in extreme circumstances">But</span>')



        for pronoun in [ " I ", " me ", "myself", "I've", "I'm" "I'd", "yourself", " yours ", " my ", " mine ", " your ", "you've", "you'll", " you ", "You "]:
            document = document.replace(pronoun, '&nbsp;<span class="pronoun" style="border:2px #f0ad4e solid" title="Effectively use 1st and 2nd person when the writing\'s about a specific person."> %s </span>&nbsp;' % pronoun)
        for entity in self.named_entity_set:
            if entity in document:
                document = document.replace(entity, '<span class="entity" style="border:2px #5cb85c solid" title="recognized name">%s</span>' % entity)
        # for p in [', ', '; ', ': ']:  # inserts these marks where they were not
        #     if p in document:
        #         document = document.replace(p, '<strong><mark>%s</mark></strong>' % p)
        for word in self.unrecognized_words:
            if word == 'th':
                pass
            elif word in document:
                #am is not getting found
                 document = document.replace(word, '&nbsp;<span class="unrecognized" style="border:2px #f0ad4e solid" title="unrecognized word"> %s </span> &nbsp; ' % word )
        for word in [" am ", " is ", " are ", " was ", ' were ', ' be ', ' being ', ' been ', ' can ', ' could ', ' shall ', ' should ', ' will ', ' would ', ' do ', ' does ', ' did ', ' may ', ' might ', ' must ', ' has ', ' have ', ' had ' ]:
            if word in document:
                document = document.replace(word, '<span class="weak" style="border:2px #d9534f solid" title="work to rely on words that convey activity">%s</span>' % word)
        #document.replace(' am ', '<span class="weak" style="border:2px #d9534f solid" title="weak verb">  am  </span>')
        # if self.very_count > 1:
        #     document = document.replace("very ", '<span class="very" style="border:2px #d9534f solid" title="Very much VERY.">very</span>')
        for word in self.tion_word_list[0]:
            document = document.replace(word, '<span class="legislatese" style="border:2px #f0ad4e solid" title="words with -tion affix quickly become overwhelming for the reader">%s</span>' % word)
        if self.very_count >= 1:
            document = document.replace(' very ', ' <span class="very" style="border:2px #f0ad4e solid" title="In most cases, VERY does not convey much. Consider deleteing.">&nbsp; very &nbsp;</span> ')
            document = document.replace('Very ', ' <span class="very" style="border:2px #f0ad4e solid" title="In most cases, VERY does not convey much. Consider deleteing.">Very &nbsp;</span> ')
        # am seems to be an extraordary problem that I can't work output
        #document = document.replace("I am ", '<span class style="border:2px #d9534f solid" title="weak verb">%s</span>' % "I am ")
        for cliche in self.cliche_list:
            document = document.replace(cliche, '<span class="label label-default cliche" title="Phrase has become cliche and lost its force.">&nbsp; %s &nbsp;</span>' % cliche)
        document += "</tbody></table></div>"

        return document
'''
