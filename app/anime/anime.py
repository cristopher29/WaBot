#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.bot import bot
import json, random, requests, xmltodict, re
from collections import OrderedDict
from bs4 import BeautifulSoup
from app.passwords import MAL_PASS,MAL_USER

with open('app/assets/json/anime.json') as data_file:
    data = json.load(data_file)

class Anime(object):
    def __init__(self, instance, conversation,param=None):
        self.instance = instance
        self.conversation = conversation
        self.anime = None
        self.build(param)

    def build(self,param):
        if param:
            if param == 'season':
                self.anime = anime_season()
                anime_lower = clean_title(self.anime['title'])
                image_path = get_image(self.anime['image_url'], anime_lower)
                self.anime['image_url'] = image_path
            else:
                self.anime = anime_search(param)

        else:
            anime = random.choice(data)
            genres = ", ".join(str(x) for x in anime['genres'])
            title = anime['canonicalTitle']
            self.anime = anime_search(title)
            self.anime['genres'] = genres


    def send_anime(self):
        if not self.anime:
            bot.send_message(self.instance,"*No he encontrado nada* :(" , self.conversation)
        else:
            text = u"*"+self.anime['title']+"* \n*Episodios*: " + self.anime['eps'] + "\n*Géneros*: " + self.anime['genres']
            bot.send_image(self.instance, self.conversation, self.anime['image_url'], text)

        


def get_image(url, caption):
    path = "app/assets/images/" + caption + ".jpg"
    file = open(path, 'wb')
    file.write(requests.get(url).content)
    file.close()
    return path

def clean_title(anime_title):
    anime_lower = anime_title.lower().replace(" ", "_")
    anime_lower = re.sub(r"/!^;.:¿¡", "", anime_lower)
    return anime_lower


def anime_search(title):

    anime_lower = clean_title(title)
    api = requests.get('https://myanimelist.net/api/anime/search.xml?q=' + anime_lower, auth=(MAL_USER, MAL_PASS))

    if api.status_code != 204:
        xml_dict = xmltodict.parse(api.content)
        input_dict = OrderedDict(xml_dict)
        output_dict = json.loads(json.dumps(input_dict))
        anime = output_dict['anime']['entry']

        if type(anime) is list:
            anime = anime[0]

        anime_dict = {
            'title' : anime['title'],
            'genres': '',
            'eps' : str(anime['episodes']),
            'image_url' : get_image(anime['image'], anime_lower)
        }

        return anime_dict

    else:
        return False


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
