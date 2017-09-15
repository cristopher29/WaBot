#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib

class Cleverbot(object):
    """Handles a conversation with Cleverbot.
    http://www.cleverbot.com/apis
    """
    def __init__(self, key, q='Hola'):
        self.HOST = "www.cleverbot.com"

        self.PROTOCOL = "https://"
        self.RESOURCE = "/getreply"

        self.key = key
        self.inital_q = urllib.quote_plus(q)

        self.SERVICE_URL = self.PROTOCOL + self.HOST + self.RESOURCE + "?key=" + self.key + "&input=" + self.inital_q
        r = requests.get(self.SERVICE_URL)
        content = r.json()
        self.cs = content['cs']
        self.conversation_id = content['conversation_id']
        self.session = requests.Session()

    def ask(self, q):
        question = urllib.quote_plus(q.strip().encode('utf8'))
        url = self.SERVICE_URL + "&input=" + question + "&cs=" + self.cs

        r = requests.get(url).json()
        return r['output']

