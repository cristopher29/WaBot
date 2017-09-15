#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, random, re
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

    def send_noticia_anime(self):
        text = u"*" + self.noticia['title'] + "*\n" + self.noticia['body'] + "\n" + self.noticia['link']
        title_lower = re.sub('[\\\\/:+*?"`<>&!-.;#€~$%|]', '', self.noticia['title'].replace(" ", "_"))
        image_url = get_image(self.noticia['image_url'],title_lower)
        bot.send_image(self.instance, self.conversation, image_url, text)


def get_image(url, caption):
    path = "app/assets/images/" + caption + ".jpg"
    file = open(path, 'wb')
    file.write(requests.get(url).content)
    file.close()
    return path


def get_noticia(tipo):

    url = ''

    if tipo == 'ciencia':
        url = 'https://www.meneame.net/m/ciencia/queue'
    elif tipo == 'videojuegos':
        url = 'https://www.meneame.net/m/videojuegos/queue'
    elif tipo == 'series':
        url = 'https://www.meneame.net/m/series/queue'
    elif tipo == 'música'.decode('utf8'):
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
            'title': title.strip(),
            'body': body.strip(),
            'link': link
        }
        news_list.append(out)

    return random.choice(news_list)