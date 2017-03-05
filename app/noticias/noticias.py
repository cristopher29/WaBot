#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, random
from app.bot import bot
from bs4 import BeautifulSoup

class Noticias(object):
    def __init__(self, instance, conversation, tipo):
        self.instance = instance
        self.conversation = conversation
        self.noticia = {}
        self.build(tipo)

    def build(self, tipo):
        self.noticia = get_noticia(tipo)

    def send_noticia(self):
        bot.send_message(self.instance, "*" + self.noticia['title'] + "*\n" + self.noticia['body'] + "\n" + self.noticia['link'], self.conversation)

def get_noticia(tipo):

    url = ''

    if tipo:
        if tipo == 'ciencia':
            url = 'https://www.meneame.net/m/ciencia/queue'
        elif tipo == 'games':
            url = 'https://www.meneame.net/m/videojuegos/queue'
        elif tipo == 'series':
            url = 'https://www.meneame.net/m/series/queue'
        elif tipo == 'música':
            url = 'https://www.meneame.net/m/M%C3%BAsica/queue'
        elif tipo == 'actualidad':
            url = 'https://www.meneame.net/m/actualidad/queue'

    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")

    news = html.find('div',{'id': 'newswrap'}).find_all('div',{'class':'news-summary'})

    news_list = []

    for new in news:
        title = new.find('h2').find('a').getText()
        body = new.find('div',{'class': 'news-content'}).getText()
        link = new.find('span', {'class': 'showmytitle'})['title']
        out = {
            'title': title,
            'body': body,
            'link': link
        }
        news_list.append(out)

    return random.choice(news_list)