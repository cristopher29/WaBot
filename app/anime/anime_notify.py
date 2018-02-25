#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.bot import bot
import requests, shutil
from bs4 import BeautifulSoup
from app.utils import helper

class AnimeNotify(object):

    def __init__(self, layer ,param=None):
        self.layer = layer
        self.last_anime_list = self.get_current_episodes()

    def get_current_episodes(self):
        url = 'https://animeflv.net/'
        req = requests.get(url)
        html = BeautifulSoup(req.text, "html.parser")

        animeList = html.find('ul', {"class": "ListEpisodios"})
        animes = animeList.findAll('li')

        anime_current = []
        for anime in animes:
            image = 'https://animeflv.net' + anime.find('img')['src']
            path = helper.get_image(image, image.rsplit('/', 1)[-1].split('.')[0])
            text = anime.find('strong').getText() + ", " + anime.find('span', {'class': 'Capi'}).getText()
            anime_current.append({'text':text,'image': path})

        return anime_current

    def update_and_notify(self, number):
        new = self.get_current_episodes()
        diff = [x for x in new if x not in self.last_anime_list]
        if (len(diff) > 0):
            print("----------------------------------")
            print("Enviando nuevos episodios")
            self.last_anime_list = new
            for anime in diff:
                bot.send_image(self.layer,number,anime['image'],"NUEVO EPISODIO!!\n"+anime['text'])
                #bot.send_message(self.layer, "NUEVO EPISODIO!!\n" + anime['text'], number)
        else:
            print("----------------------------------")
            print("No hay nuevos episodios")

