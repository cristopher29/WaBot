#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from app.bot import bot


class Chiste(object):
    def __init__(self, instance, conversation):
        self.instance = instance
        self.conversation = conversation
        self.chiste = ''
        self.build()

    def build(self):
        url = 'http://pagina-del-dia.euroresidentes.es/chiste-del-dia/gadget-chiste-del-dia.php?modo=2'
        req = requests.get(url)
        html = BeautifulSoup(req.text, "html.parser")
        text = html.find('td', {'bgcolor': '#FFFFFF'}).getText().strip()
        self.chiste = text.encode('latin1').decode('utf8').split('\n')

        out = ''
        for s in self.chiste:
            s = s.strip().rstrip('\r\n')
            if s:
                out += '*'+s+'*\n'
        print out
        self.chiste = out.strip()

    def send_chiste(self):
        bot.send_message(self.instance, self.chiste , self.conversation)