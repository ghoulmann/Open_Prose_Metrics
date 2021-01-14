#external tools: textgain

import requests
import json

def sentiment_result(text):
    URL = 'http://text-processing.com/api/sentiment/'
    raw_text = text
    r = requests.post(URL, data = {'text':raw_text})
    sentiment = json.loads(r.text).get('label')
    return sentiment
