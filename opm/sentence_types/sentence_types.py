from nltk.tag import pos_tag

from nltk.tokenize import word_tokenize, sent_tokenize
#from nltk.tokenize import sent_tokenize

class SentenceTypes():
    def __init__(self, bag_o_sents):
        self.coords = ['for', 'and', 'nor', 'but', 'or', 'yet', 'so']
        self.transitions = [
            'in the first place',
            'not only ... but also',
            'as a matter of fact',
            'in like manner',
            'in addition',
            'coupled with',
            'in the same fashion',
            'in the same way',
            'first',
            'second',
            'third',
            'in the light of',
            'not to mention',
            'to say nothing of',
            'equally important',
            'by the same token',
            'again',
            'to',
            'also',
            'then',
            'equally',
            'identically',
            'uniquely',
            'like',
            'as',
            'too',
            'moreover',
            'as well as',
            'together with',
            'of course',
            'likewise',
            'comparatively',
            'correspondingly',
            'similarly',
            'furthermore',
            'additionally',
            'although this may be true',
            'in contrast',
            'different from',
            'of course',
            'on the other hand',
            'on the contrary',
            'at the same time',
            'in spite of',
            'even so',
            'though',
            'be that as it may',
            'then again',
            'above all',
            'in reality',
            'after all',
            'still',
            'and still',
            'unlike',
            'or',
            'and yet',
            'yet',
            'while',
            'albeit',
            'besides',
            'as much as',
            'even though',
            'although',
            'instead',
            'whereas',
            'despite',
            'conversely',
            'otherwise',
            'however',
            'rather',
            'nevertheless',
            'nonetheless',
            'regardless',
            'notwithstanding',
            'in the event that',
            'granted that',
            'granted',
            'so long as',
            'on the condition that',
            'on condition',
            'for the purpose of',
            'for the purposes of',
            'with this intention',
            'with this in mind',
            'in the hope that',
            'to the end that',
            'for fear that',
            'in order to',
            'seeing that',
            'being that',
            'in view of',
            'If',
            'then',
            'unless',
            'when',
            'whenever',
            'while',
            'because of',
            'as',
            'since',
            'while',
            'lest',
            'in case',
            'provided that',
            'given that',
            'only if',
            'even if',
            'so that',
            'so as to',
            'owing to',
            'inasmuch as',
            'due to',
            'in other words',
            'to put it differently',
            'for one thing',
            'as an illustration',
            'in this case',
            'for this reason',
            'to put it another way',
            'that is to say',
            'with attention to',
            'by all means',
            'important to realize',
            'another key point',
            'first thing to remember',
            'most compelling evidence',
            'must be remembered',
            'point often overlooked',
            'to point out',
            'on the positive side',
            'on the negative side',
            'with this in mind',
            'notably',
            'including',
            'like',
            'to be sure',
            'namely',
            'chiefly',
            'truly',
            'indeed',
            'certainly',
            'surely',
            'markedly',
            'such as',
            'especially',
            'explicitly',
            'specifically',
            'expressly',
            'surprisingly',
            'frequently',
            'significantly',
            'particularly',
            'in fact',
            'in general',
            'in particular',
            'in detail',
            'for example',
            'for instance',
            'to demonstrate',
            'to emphasize',
            'to repeat',
            'to clarify',
            'to explain',
            'to enumerate',
            'as a result',
            'under those circumstances',
            'in that case',
            'for this reason',
            'in effect',
            'for',
            'thus',
            'because the',
            'then',
            'hence',
            'consequently',
            'therefore',
            'thereupon',
            'forthwith',
            'accordingly',
            'henceforth',
            'as can be seen',
            'generally speaking',
            'in the final analysis',
            'all things considered',
            'as shown above',
            'in the long run',
            'given these points',
            'as has been noted',
            'in a word',
            'for the most part',
            'after all',
            'in fact',
            'in summary',
            'in conclusion',
            'in short',
            'in brief',
            'in essence',
            'to summarize',
            'on balance',
            'altogether',
            'overall',
            'ordinarily',
            'usually',
            'by and large',
            'to sum up',
            'on the whole',
            'in any event',
            'in either case',
            'all in all',
            'Obviously',
            'Ultimately',
            'Definitely',
            'at the present time',
            'from time to time',
            'sooner or later',
            'at the same time',
            'up to the present time',
            'to begin with',
            'in due time',
            'as soon as',
            'as long as',
            'in the meantime',
            'in a moment',
            'without delay',
            'in the first place',
            'all of a sudden',
            'at this instant',
            'first',
            'second',
            'immediately',
            'quickly',
            'finally',
            'after',
            'later',
            'last',
            'until',
            'till',
            'since',
            'then',
            'before',
            'hence',
            'since',
            'when',
            'once',
            'about',
            'next',
            'now',
            'formerly',
            'suddenly',
            'shortly',
            'henceforth',
            'whenever',
            'eventually',
            'meanwhile',
            'further',
            'during',
            'in time',
            'prior to',
            'forthwith',
            'straightaway',
            'by the time',
            'whenever',
            'until now',
            'now that',
            'instantly',
            'presently',
            'occasionally',
            'in the middle',
            'to the left',
            'to the right',
            'in front of',
            'on this side',
            'in the distance',
            'here and there',
            'in the foreground',
            'in the background',
            'in the center of',
            'adjacent to',
            'opposite to',
            'here',
            'there',
            'next',
            'where',
            'from',
            'over',
            'near',
            'above',
            'below',
            'down',
            'up',
            'under',
            'further',
            'beyond',
            'nearby',
            'wherever',
            'around',
            'between',
            'before',
            'alongside',
            'amid',
            'among',
            'beneath',
            'beside',
            'behind',
            'across',
        ]
        self.subs = [
            'after',
            'although',
            'as',
            'as if',
            'as long as',
            'as much as',
            'as soon as',
            'as though',
            'because',
            'before',
            'by the time',
            'despite',
            'during',
            'even if',
            'even though',
            'even with',
            'from',
            'had',
            'hence',
            'having'
            'however',
            'if',
            'in order that'
            'in case',
            'in fact'
            'in the event that',
            'later',
            'lest',
            'moreover',
            'nevertheless',
            'now that',
            'once',
            'only',
            'only if',
            'provided that',
            'simultaneously',
            'since',
            'so',
            'supposing',
            'that',
            'than',
            "thereby"
            'though',
            'throughout',
            'thus',
            'thereby'
            'therefore',
            'till',
            'throughout',
            'unless',
            'until',
            'when',
            'whenever',
            'where',
            'whereas',
            'wherever',
            'whether or not',
            'while',
            'with',
            'without']

        self.complex_sents = []
        self.problem_sents = []
        self.compound_complex_sents = []
        self.compound_sents = []
        self.appositive_sents = []
        self.transSentences = []
        self.list_sents = []
        self.simple_sents = []
        self.coord_start_sents = []
        self.sentence_bag = sent_tokenize(bag_o_sents)
        self.gerund_sents = []

        
        #self.filter_sents()
        self.otherPunct()
        self.gatherSubs()
        self.isolateTransitions()
        self.catCoords()
        self.isolateAppositives()
        self.isolateLists()
        self.isolateProblems()
        self.recoverProblems()
    
    
    
    def otherPunct(self):
        for sent in self.sentence_bag:
            if "; " in sent:
                self.problem_sents.append(sent)
                self.sentence_bag.remove(sent)
            elif ": " in sent:
                self.problem_sents.append(sent)
                self.sentence_bag.remove(sent)
            else:
                pass

    # process subordinating conjunctions and sents that start with gerunds
    def gatherSubs(self):
        for sent in self.sentence_bag:
            tokens = word_tokenize(sent)
            tags = pos_tag(tokens)
            if tags[0][1] == 'IN':
                self.complex_sents.append(sent)
                self.sentence_bag.remove(sent)
        for sent in self.sentence_bag:
            tokens = word_tokenize(sent)
            tags = pos_tag(tokens)
            if tags[0][1] == 'VBG':
                self.gerund_sents.append(sent)
                self.sentence_bag.remove(sent)
        for conj in self.subs:
            for sent in self.sentence_bag:
            
            
                if conj.capitalize() in sent:
                    self.complex_sents.append(sent)
                    self.sentence_bag.remove(sent)
        for sent in self.complex_sents:
            if ", " not in sent:
                self.complex_sents.remove(sent)
                self.problem_sents.append(sent)
    def isolateTransitions(self):
        for tran in self.transitions:
            for sent in self.sentence_bag:
                if tran.capitalize() in sent:
                    self.complex_sents.append(sent)
                    self.sentence_bag.remove(sent)
    def catCoords(self):
        for sent in self.sentence_bag:
            if (", and ") in sent or (", or ") in sent:
                if sent.count(", ") >= 2:
                    self.list_sents.append(sent)
                    self.sentence_bag.remove(sent)
        for conj in self.coords:
            for sent in self.sentence_bag:
                if conj.capitalize() in sent:
                    self.coord_start_sents.append(sent)
                    try:
                        self.sentence_bag.remove(sent)
                    except ValueError:
                        print("X-ray produced ValueError at \"%\"" % sent)
                        
                if (", " + conj + " ") in sent:
                    self.compound_sents.append(sent)
                    try:
                        self.sentence_bag.remove(sent)
                    except ValueError:
                        print("X-ray produced ValueError at \"%s\"" % sent)
        """for sent in self.complex_sents:  
            if ", and " in sent or ", or " in sent:
                if sent.count(", ") == 2:
                    self.compound_complex_sents.append(sent)
                    self.complex_sents.remove(sent)
                elif sent.count(", ") > 2:
                    self.problem_sents.append(sent)
                    self.complex_sents.remove(sent)
        for sent in self.complex_sents:    
            for conj in self.coords:  
                if ", " + conj + " " in sent:
                    if sent.count(", ") == 2:
                        self.compound_complex_sents.append(sent)
                        self.complex_sents.remove(sent)
        for sent in self.complex_sents:    
            for conj in self.coords:
                if sent.count(", ") > 2:
                    self.list_sents.append(sent)
                    self.complex_sents.remove(sent) """
    def isolateAppositives(self):
        for sent in self.sentence_bag:
            if sent.count(", ") == 2:
                self.appositive_sents.append(sent)
                self.sentence_bag.remove(sent) 
    def isolateLists(self):
        for sent in self.sentence_bag:
            if  ", and " in sent  or ", or " in sent:
                if sent.count(", ") > 2:
                    self.list_sents.append(sent)
                    self.sentence_bag.remove(sent)
        for sent in self.complex_sents:
            if (", and " in sent or ", or " in sent):
                if sent.count(", ") > 2:
                    self.list_sents.append(sent)
                    self.complex_sents.remove(sent)
    def isolateProblems(self):
        for sent in self.sentence_bag:
            self.problem_sents.append(sent)
            self.sentence_bag.remove(sent)
    def recoverProblems(self):
        for sent in self.problem_sents:
            for conj in self.subs:
                if ", " + conj in sent:
                    self.complex_sents.append(sent)
                    if sent in self.problem_sents:
                        self.problem_sents.remove(sent)
        for tran in self.transitions:
            for sent in self.problem_sents:
                if ", " + tran in sent:
                    self.complex_sents.append(sent)
                    self.problem_sents.remove(sent)
