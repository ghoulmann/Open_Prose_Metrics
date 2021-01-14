from objdict import ObjDict

Doc.serialized = ObjDict()
Doc.serialized.identification = Doc.file_name + " " + Doc.time_stamp
Doc.serialized.statistics = {
    "Word Count": Doc.lexicon_count,
    "Page Count": Doc.page_count,
    "Polysyllables": Doc.polysyllables,
    "Average Sentence Length": Doc.average_sentence_length
    }
Doc.serialized.readability = {
    "Readability Standard": Doc.readability_standard,
    "Reading Difficulty": Doc.flesch_re_key
    }
Doc.serialized.concision = {
        "To Be Verb Count": Doc.be_verb_count,
        "To Be Proportion": Doc.weak_verbs_to_sentences_round,
        "Other Modals": Doc.modals,
        "Percent Passive": Doc.percent_passive_round,
        "Weak Verb Example": Doc.rand_weak_sentence,
        "Passive Example": Doc.rand_passive
    }
