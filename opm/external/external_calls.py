#external tools: text-processing.com


import requests
import json

def entities(text):
    URL = 'http://text-processing.com/api/phrases/'
    raw_text = text
    r = requests.post(URL, data = {'text':raw_text})
    try:
        entities = json.loads(r.text).get('location')
        return entities
    except:
        pass
        #print "could not return entities"
