from transitions.transitions import transitions

# def categorizeCommaSents(object):
#     commaSents = (object.sentences)
#     return commaSents

def annotateStyle(object):
    #coords = object.sentenceStructures.coords
    #subs = object.sentenceStructures.subs

    d = []
    #markup = u""
    for s in object.sentence_tokens:
        if s in object.passive_sentences:
            d.append([s, "passive"])
        elif s in object.weak_sentences:
            d.append([s, "weak"])
        else:
            d.append([s, "pass"])
    for s in d:
        #sentence comma usage

        # if s[0] in object.apposSents:
        #     s[0] += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">Appositive</span>'
        # elif s[0] in object.complexSents:
        #     s[0] += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">Complex</span>'
        # elif s[0] in object.compoundSents:
        #     s[0] += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">Compound</span>'
        # elif s[0] in object.listSents:
        #     s[0] += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">List</span>'
        # elif s[0] in object.problemSents:
        #     s[0] += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-warning pull-right">Unidentified Structure</span>'
        # elif s[0] in object.transitionSents:
        #     s[0] += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">Transitional Phrase</span>'
        # elif s[0] in object.compComplexSents:
        #     s[0] += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">Compound-Complex</span>'
        # else:
        #     pass
        ### For Weasel Words ### Disabled because it disrupts all other annotations
        # for w in set(object.weasel_words):
        #        if " " + w + " " in s[0]:
        #           s[0] = s[0].replace(" " + w + " ", '&nbsp;<span class="weasel" style=border:2px #337ab7 solid;" title="weasel word: lacks commitment"> %s  </span>&nbsp;' % w)
        # Start with But
        # s[0] = s[0].replace("But ", '<span style="border:2px #d9534f solid" title="Start with But only in extreme circumstances" class="but">But</span>&nbsp;')


        for c in object.cliche_list:
            s[0] = s[0].replace(c, '<span class="cliche" style="border:2px #f0ad4e solid" title="Overused phrase lost its power">%s</span>' % c)
        # Highlight transitional phrases
        # for trans in transitions:
        #     if "as" not in trans:
        #         s[0] = s[0].replace(trans, '<span style="color:green;">%s</span>' % trans)
        #for entity in object.named_entity_set:
        #    if (" " + entity + " ") in s[0]:
        #        s[0] = s[0].replace(entity, '<span class="named-entity" style="border:2px #5cb85c solid" title="recognized entity">&nbsp; %s &nbsp; </span>' % entity)
        for word in set(object.unrecognized_words):
            if (" " + word + " ") in s[0]:
                s[0] = s[0].replace(word, '&nbsp;<span class="unrecognized" style="border:2px #f0ad4e solid" title="unrecognized word">%s</span>&nbsp;' % word)
        for w in set(object.tion_word_list[0]):
            s[0] = s[0].replace(" " + w + " ", '&nbsp;<span class="legislatese" style="border:2px #f0ad4e solid" title="words with -tion affix quickly become overwhelming for the reader">%s</span>&nbsp;' % w)

        if object.very_count > 1:
            s[0] = s[0].replace(" very ", '&nbsp; <span class="very" style=border:2px #f0ad4e solid" title="Usually adds nothing to a sentence">very</span>&nbsp;')
        for m in [ ' can ', ' could ', ' shall ', ' should ', ' would ', ' do ', ' does ', ' did ', ' may ', ' might ', ' must ', ' shall ', ' will ',  ' has ', ' have ', ' had ']:
            s[0] = s[0].replace(m, '&nbsp;<span class="weak" style="border:2px #d9534f solid" title="work to rely on words that convey activity">%s</span>&nbsp;' % m)
        for p in [' am ', ' is ', ' are ', ' was ', ' were ', ' be ', ' being ', ' been ']:
            s[0] = s[0].replace(p, '&nbsp;<span class="weak" style="border:2px #d9534f solid" title="work to rely on words to convey action">%s</span>&nbsp;' % p)
        for pp in [ " you ", "you\'ll", " your ", " yourself ", " yours ", " you\'re "]:
            s[0] = s[0].replace(pp, '&nbsp;<span class="voice">%s</span>&nbsp;' % pp)
        for pp in [ "I ", " me ", "myself", "I've", "I'm", "I'd", "yourself", " yours ", " my ", " mine ", " your ", "you've", "you'll", " you ", "You "]:
            if pp in s[0]:
                s[0] = s[0].replace(pp, '&nbsp;<span class="voice" style="border:2px #f0ad4e solid" title="Effectively use 1st and 2nd person when the writing\'s about a specific person.">%s</span>&nbsp;' % pp)


        # sentence nominalization labels
        if s[1] == "passive":
            s[0] += '&nbsp;<span style="font-size:13pt" class="label label-large label-danger pull-right">Passive</span>'
        elif s[1] == "weak":
            s[0] += '&nbsp;<span style="font-size:13pt" class="label label-large label-danger pull-right">Weak Verb(s)</span>'
        else:
            pass





    return d

def annotateStructure(object):
    coords = object.sentenceStructures.coords
    subs = object.sentenceStructures.subs
    trans = transitions
    d = []
    for s in object.sentences:
        if s in object.apposSents:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-warning pull-right">Possible Appositive or Absolute Phrase: Eval Manually</span>'
            d.append([s, "appositive"])
        elif s in object.complexSents:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">Dependent Clause, check against Comma Convention</span>'
            d.append([s, "complex"])
        elif s in object.compoundSents:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">Coord. Conjunction immediately following a Comma (possibly a list, however)</span>'
            d.append([s, "compound"])
        elif s in object.listSents:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-warning pull-right">Possibly a List: Please Evaluate</span>'
            d.append([s, "list"])
        elif s in object.problemSents:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-warning pull-right">Simple Sentence, Fragment, or unexpected punctuation sequence</span>'
            d.append([s, "problem"])
        elif s in object.transitionSents:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">Initial Transitional Phrase</span>'
            d.append([s, "transitional"])
        elif s in object.compComplexSents:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">Compound-Complex Structure</span>'
            d.append([s, "compound-complex"])
        elif s in object.coordProblems:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-danger pull-right">Unconventional Start (Coordinating Conjunction in first position)</span>'
            d.append([s, "bad_start"])
        elif s in object.gerundSents:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-danger pull-right">Initial Gerund: Check for comma usage</span>'
            d.append([s, "gerund"])
        # elif s in object.listSents:
        #     s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-default pull-right">list</span>'
        else:
            s += '&nbsp;<span style="font-size:13pt; margin-left:8px;" class="label label-large label-success pull-right">Unidentified Structure: Check Context and Voice</span>'
            d.append([s, "ok"])
    final = []
    for s in d:
        for tr in trans:
            if s[1] == "transitional":
                s[0] = s[0].replace(", " + tr + " ", ', <span title="transitional word/phrase" style="border:grey .5px solid">%s</span> ' % tr)
                s[0] = s[0].replace(tr.capitalize() + " ", '<span title="transitional word/phrase" style="border:grey .5px solid">%s</span>&nbsp;' % tr.capitalize())
                #s = s.replace(" " + tr + ", ", " <mark>%s</mark>, " % tr)
                s[0] = s[0].replace(tr.capitalize() + '&nbsp;', '<span title="transitional word/phrase" style="border:grey .5px solid">%s</span>,&nbsp;' % tr.capitalize())

            else:
                pass

        for c in coords:
            if c in s:
                if s[1] == "compound":
                    s[0] = s[0].replace(", " + c + " ", ', <span title="coordinating conjunction" style="border:#00C851 .5px solid">%s</span>&nbsp;' % c)
            if c == "and" or c == "or":
                if s[1] == "list":
                    s[0] = s[0].replace(", " + c + " ", ',&nbsp;<span title="coordinating conjunction" style="border:#00C851 .5px solid">%s</span> ' % c)
            s[0].replace(', ', '<mark>,&nbsp;</mark>')
        for c in subs:
            if c in s:
                if s[1] == "complex":
                    s[0] = s[0].replace(c.capitalize() + "&nbsp;", '<span title="subordinating conjunction" style="border:#00C851 .5px solid">%s</span> ' % c.capitalize())
                    s[0] = s[0].replace(", " + c, ', <span title="subordinating conjunction" style="border:#00C851 .5px solid">%s</span> ' % c)
                    s[0] = s[0].replace(c.capitalize() + ", ", '<span title="subordinating conjunction" style="border:green .5px solid">%s</span> '  % c)
                else:
                    pass

        final.append(s)

        ### For Weasel Words ### Disabled because it disrupts all other annotations
        # for w in set(object.weasel_words):
        #        if " " + w + " " in s[0]:
        #           s[0] = s[0].replace(" " + w + " ", '&nbsp;<span class="weasel" style=border:2px #337ab7 solid;" title="weasel word: lacks commitment"> %s  </span>&nbsp;' % w)
        # Start with But
        # s[0] = s[0].replace("But ", '<span style="border:2px #d9534f solid" title="Start with But only in extreme circumstances" class="but">But</span>&nbsp;')



        # Highlight transitional phrases
        # for trans in transitions:
        #     if "as" not in trans:
        #         s[0] = s[0].replace(trans, '<span style="color:green;">%s</span>' % trans)
        #for entity in object.named_entity_set:
        #    if (" " + entity + " ") in s[0]:
        #        s[0] = s[0].replace(entity, '<span class="named-entity" style="border:2px #5cb85c solid" title="recognized entity">&nbsp; %s &nbsp; </span>' % entity)
        # for word in set(object.unrecognized_words):
        #     if (" " + word + " ") in s:
        #         s = s.replace(word, '&nbsp;<span class="unrecognized" style="border:2px #f0ad4e solid" title="unrecognized word">%s</span>&nbsp;' % word)
        #
        #
        # if object.very_count > 1:
        #     s = s.replace(" very ", '&nbsp; <span class="very" style=border:2px #f0ad4e solid" title="Usually adds nothing to a sentence">very</span>&nbsp;')





        # sentence nominalization labels
        # if s[1] == "passive":
        #     s[0] += '&nbsp;<span style="font-size:13pt" class="label label-large label-danger pull-right">Passive</span>'
        # elif s[1] == "weak":
        #     s[0] += '&nbsp;<span style="font-size:13pt" class="label label-large label-danger pull-right">Weak Verb(s)</span>'
        # else:
        #     pass





    return final
