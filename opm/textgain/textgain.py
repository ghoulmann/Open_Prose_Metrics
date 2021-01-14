u"""
Query textgain.com for age, gender, or education associated with prose.
"""



from __future__ import absolute_import
import json
import requests


def textgain(call, raw_text, language=u'en'):
    if call == u'gender':
        url = u'https://api.textgain.com/1/gender'
    elif call == u'education':
        url = u'https://api.textgain.com/1/education'
    elif call == u'personality':
        url = u'https://api.textgain.com/1/personality'
    elif call == u'age':
        url = u'https://api.textgain.com/1/age'
    elif call == u'sentiment':
        url = u'https://api.textgain.com/1/sentiment'
    elif call == u'genre':
        url = u'https://api.textgain.com/1/genre'
    elif call == u'concepts':
        url = u'https://api.textgain.com/1/concepts'
    else:
        return u"Call not specified"

    try:
        r = requests.post(url, data={u'q':raw_text, u'lang':language})
        return json.loads(r.text).get(call)
    except:
        print (u"Textgain - %s failed - probably too many requests." % call)
