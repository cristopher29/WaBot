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
            title = anime['canonicalTitle']
            genres = ", ".join(str(x) for x in anime['genres'])
            self.anime = anime_search(title, genres=genres)


    def send_anime(self):
        if not self.anime:
            bot.send_message(self.instance,"*No he encontrado nada* :(" , self.conversation)
        else:
            text = "*"+self.anime['title']+"* \n*Episodios*: " + self.anime['eps'] + "\n*Géneros*: ".decode('utf8') + self.anime['genres'] + ""
            bot.send_image(self.instance, self.conversation, self.anime['image_url'], text)

        


def get_image(url, caption):
    path = "app/assets/images/" + caption + ".jpg"
    with open(path, 'wb') as file:
        file.write(requests.get(url).content)
    return path

def clean_title(anime_title):
    regex = re.compile('[^0-9a-zA-Z]')
    title = regex.sub("%20", anime_title)
    return title


def anime_search(title, genres=None):

    anime_lower = clean_title(title)
    url = 'https://myanimelist.net/search/all?q=' + anime_lower

    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")
    result = html.findAll('a' , {'class': 'hoverinfo_trigger'})

    if result and 'https://myanimelist.net/anime/' in result[0]['href']:
        req = requests.get(result[0]['href'])
        html = BeautifulSoup(req.text, "html.parser")

        anime_title = html.find('h1',{'class': 'h1'}).find('span').getText()

        sidebar = html.find('div',{'class':'js-scrollfix-bottom'})

        anime_image = sidebar.find('img')['src']

        information = sidebar.find_all('div',{'class':'spaceit'})[0].getText()
        anime_eps = information.replace('Episodes:','').strip()

        genres_tags = html.findAll('a', attrs={'href': re.compile('/anime/genre/*')})
        genres_out = ''
        for genre in genres_tags:
            genres_out += genre.getText() + ", "
        anime_genres = genres_out[:-2]


        anime_dict = {
            'title': anime_title,
            'genres': anime_genres,
            'eps': anime_eps,
            'image_url': get_image(anime_image, anime_title.replace(' ', '_'))
        }
        return anime_dict
    else:
        return 'No hay nada'


def anime_season():
    url = 'https://myanimelist.net/anime/season'
    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")

    animes_temp = html.find('div', {
        'class': 'seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1 clearfix'}).find_all('div', {
        'class': 'seasonal-anime js-seasonal-anime'})

    anime  = random.choice(animes_temp)

    titulo = anime.find('p', {'class': 'title-text'}).find('a').getText()
    eps = anime.find('div', {'class': 'eps'}).find('span').getText()
    image_temp = anime.find('div', {'class': 'image'}).find('img')

    if image_temp.has_attr('src'):
        image_temp = image_temp['src']
    elif image_temp.has_attr('data-src'):
        image_temp = image_temp['data-src']

    image_url = re.search("(?P<url>https?://[^\s]+)", image_temp).group("url")
    genres_temp = anime.find('div', {'class': 'genres-inner js-genre-inner'}).find_all('span', {'class': 'genre'})
    genres = ''
    for genre in genres_temp:
        genres += genre.find('a').getText() + ", "

    return {
        'title': titulo,
        'genres': genres.strip()[:-1],
        'eps': eps.replace('eps', ''),
        'image_url': image_url
    }
