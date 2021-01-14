from __future__ import absolute_import
from .sentenceKeys import coords, subs, transitions

def classifySents(sentenceBag):
    listSents = []
    unidentifiedSents = []
    compoundSents = []
    compoundComplexSents = []
    complexSents = []
    sentences = SentenceBag

    #from test script
    for sent in sentenceBag:
      for coor in coords:
        if (u", " + coor) in sent:
          if sent.count(u", ") == 1:
            compoundSents.append(sent)
            sentenceBag.remove(sent)
          else:
            if (coor == u"or") or (coor == u"and"):
              listSents.append(sent)
              sentenceBag.remove(sent)
        else:
          pass
    for sent in sentenceBag:
       for tran in transit:
         if tran.capitalize() in sent:
          sentenceBag.remove(sent)
          complexSents.append(sent)
    for sent in sentenceBag:
      for sub in subs:
        if sub.capitalize() in sent.capitalize():
          complexSents.append(sent)
          sentenceBag.remove(sent)
    for sent in listSents:
      for sub in subs:
        if sub.capitalize() in sent.capitalize():
          compoundComplexSents.append(sent)
          listSents.remove(sent)
