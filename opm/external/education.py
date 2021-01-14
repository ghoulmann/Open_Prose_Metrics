#external tools: textgain

import requests
import json



def education_result(text):
        URL = 'https://api.textgain.com/1/education'

        r = requests.post(URL, data = {'q':text, 'lang':'en'})
        education = json.loads(r.text).get('education')

        if education == '+':
            return "Master's degree or above"
        else:
            return "Undergraduate degree or below"
