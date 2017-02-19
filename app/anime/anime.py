#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.bot import bot
import json, random, requests, xmltodict, re
from collections import OrderedDict
from bs4 import BeautifulSoup

with open('app/assets/json/anime.json') as data_file:
    data = json.load(data_file)

class Anime(object):
    def __init__(self, instance, conversation,season):
        self.instance = instance
        self.conversation = conversation
        self.title = ""
        self.genre = ""
        self.epis = ""
        self.image_path = ""
        self.no_anime = False
        self.build(season)

    def build(self,season):
        if season:
            anime = anime_season()
            anime_lower = anime['title'].lower().replace(" ", "_")
            anime_lower = re.sub(r"/!^;.:¿¡", "", anime_lower)
            self.title = anime['title']
            self.genre = anime['genres']
            self.epis = anime['eps']
            self.image_path = get_image(anime['image_url'], anime_lower)

        else:
            anime = random.choice(data)
            genres = ", ".join(str(x) for x in anime['genres'])
            anime_lower = anime['canonicalTitle'].lower().replace(" ", "_")
            anime_lower = re.sub(r"/!^;.:¿¡", "", anime_lower)
            api = requests.get('https://myanimelist.net/api/anime/search.xml?q=' + anime_lower, auth=('', ''))
            if api.status_code != 204:

                xml_dict = xmltodict.parse(api.content)
                input_dict = OrderedDict(xml_dict)
                output_dict = json.loads(json.dumps(input_dict))
                anime = output_dict['anime']['entry']

                if type(anime) is list:
                    anime = anime[0]

                self.image_path = get_image(anime['image'], anime_lower)
                self.title = anime['title']
                self.epis = str(anime['episodes'])
                self.genre = genres
            else:
                self.no_anime = True

    def send_anime(self):
        if self.no_anime:
            bot.send_message(self.instance,"*No he encontrado nada* :(" , self.conversation)
        else:
            text = u"*"+self.title+"* \n*Episodios*: " + self.epis + "\n*Géneros*: " + self.genre
            bot.send_image(self.instance, self.conversation, self.image_path, text)

        


def get_image(url, caption):
    path = "app/assets/images/" + caption + ".jpg"
    file = open(path, 'wb')
    file.write(requests.get(url).content)
    file.close()
    return path

def anime_season():
    url = 'https://myanimelist.net/anime/season'
    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")
    anime_s = []

    animes_temp = html.find('div', {
        'class': 'seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1 clearfix'}).find_all('div', {
        'class': 'seasonal-anime js-seasonal-anime'})

    for i, anime in enumerate(animes_temp):
        titulo = anime.find('p', {'class': 'title-text'}).find('a').getText()
        eps = anime.find('div', {'class': 'eps'}).find('span').getText()
        image_temp = anime.find('div', {'class': 'image'})['style']
        image_url = re.search("(?P<url>https?://[^\s]+)", image_temp).group("url")[:-1]
        genres_temp = anime.find('div', {'class': 'genres-inner js-genre-inner'}).find_all('span', {'class': 'genre'})

        genres = ''
        for genre in genres_temp:
            genres += genre.find('a').getText() + ", "

        dict = {
            'title': titulo,
            'genres': genres.strip()[:-1],
            'eps': eps.replace('eps', ''),
            'image_url': image_url
        }
        anime_s.append(dict)
        
    return random.choice(anime_s)
