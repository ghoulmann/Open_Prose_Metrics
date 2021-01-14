# -*- coding: utf-8 -*-

import json
import requests
from aylienapiclient import textapi


class Service:

    def __init__(self, service, config='config.json'):

        with open(config) as self.data_file:
            self.info = json.load(self.data_file)
        self.info = self.info[service]
        self.data_file = ""

class Textgain:
    def __init__(self, raw_text, language='en'):
        self.text = raw_text
        self.language = language
        #self.sex = self.gender()
        #self.url = 'https://api.textgain.com/1/gender'
        self.URL = 'https://api.textgain.com/1/'
        self.sentiment = self.make_call('sentiment')
        self.gender = self.make_call('gender')
        self.concepts = self.make_call('concepts')
        self.genre = self.make_call('genre')
        self.age = self.make_call('age')
        self.education = self.make_call('education')
        self.personality = self.make_call('personality')

    def make_call(self, call):
        self.call = call
        self.endpoint = self.URL + self.call
        self.data = {'q':self.text, 'lang':self.language}
        self.r = requests.post(self.endpoint, data=self.data)
        if self.call == 'sentiment':
            self.result = json.loads(self.r.text).get('polarity')
        else:
            self.result = json.loads(self.r.text).get(self.call)
        return self.result

class Rosette:
    def __init__(self, key, raw_text, language='en'):
        self.apikey = key
        self.text = raw_text
        self.URL = 'https://api.rosette.com/rest/v1/'
        self.sentiment = self.make_call('sentiment')
        self.categories = self.make_call('categories')
        self.entities = self.make_call('entities')
        #self.ping = self.make_call('ping')


    def make_call(self, call):
        self.call = call
        self.endpoint = self.URL + self.call
        self.data = {'content': self.text}
        self.headers = {'X-RosetteAPI-Key': self.apikey, 'Content-Type':'application/json'}
        self.r = requests.post(self.endpoint, params=self.data, headers=self.headers)

class Aylien:
    def __init__(self, key, appid):
        self.apikey = key
        self.appid = appid
        self.client = textapi(self.appid, self.apikey)

    def r(self, text):
        self.request = self.client({'text': text, 'endpoint':["hashtags", "concepts", "classify", "entities"]})
        return self.request








        #rosette_client = rosette.API(user_key=key, service_url=service)
        #return rosette_client





"""
def rosette_auth(key="390f27851d05ab470a095e6cf6441548", service='https://api.rosette.com/rest/v1/'):
    rosette_client = API(user_key=key, service_url='https://api.rosette.com/rest/v1/')
    return rosette_client
"""
