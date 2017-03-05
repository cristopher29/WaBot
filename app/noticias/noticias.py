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

    def send_noticia_anime(self):
        text = u"*" + self.noticia['title'] + "*\n" + self.noticia['body'] + "\n" + self.noticia['link']
        title_lower = self.noticia['title'].replace(" ", "_")
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
    news_list = []

    if tipo != 'anime':

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
                'title': title.strip(),
                'body': body.strip(),
                'link': link
            }
            news_list.append(out)
    else:

        url = 'http://misiontokyo.com/'
        req = requests.get(url)
        html = BeautifulSoup(req.text, "html.parser")
        news = html.find('div',{'id':'Columna1'}).find_all('div',{'class':'bord_ext_news'})

        for new in news:
            title = new.find('a',{'class':'txt_home_news'})['title']
            body = new.find('a',{'class':'txt_home_news'}).getText()
            link = new.find('a',{'class':'txt_home_news'})['href']
            image_url = new.find('img', attrs={'style': 'width:337px; height:190px; border:1px solid #000;'})['src']
            out = {
                'title': title.strip(),
                'body': body.strip(),
                'link': link,
                'image_url': image_url
            }


            news_list.append(out)

        url = 'http://ramenparados.com/category/noticias/anime/'
        req = requests.get(url)
        html = BeautifulSoup(req.text, "html.parser")
        news = html.find('ul', {'class': 'widget-full1 left relative infinite-content'}).find_all('li')

        for new in news:
            title = new.find('div',{'class':'widget-full-list-text'}).find('a').getText()
            body = new.find('div',{'class':'widget-full-list-text'}).find('p').getText()
            link = new.find('div',{'class':'widget-full-list-text'}).find('a')['href']
            image_url = new.find('img',{'class':'attachment-medium-thumb size-medium-thumb wp-post-image'})['data-lazy-src']
            out = {
                'title': title.strip(),
                'body': body.strip(),
                'link': link,
                'image_url': image_url
            }

            news_list.append(out)

        url = 'https://animanga.es'
        req = requests.get(url)
        html = BeautifulSoup(req.text, "html.parser")
        news = html.find('div', {'class': 'n'}).find_all('article')

        for new in news:
            title = new.find('h3').find('a').getText()
            body = new.find('p').getText()
            link = new.find('figure').find('a')['href']
            image_url = new.find('figure').find('img')['src']
            out = {
                'title': title.strip(),
                'body': body.strip(),
                'link': link,
                'image_url': url+image_url
            }

            news_list.append(out)

    #random.shuffle(news_list)
    return random.choice(news_list)