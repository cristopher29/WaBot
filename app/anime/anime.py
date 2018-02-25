#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.bot import bot
import json, random, requests, xmltodict, re
from bs4 import BeautifulSoup
from app.utils import helper


with open('app/assets/json/anime.json') as data_file:
    data = json.load(data_file)

waiting_respond = {}

class Anime(object):
    def __init__(self, instance, conversation, person, param=None, num=None):
        self.instance = instance
        self.conversation = conversation
        self.anime = []
        self.person = person
        self.param = param
        self.num = num
        self.build()

    def build(self):
        if self.param:
            print("Parametro anime: " + self.param)
            if self.param == 'season_num':
                if self.num.isdigit():
                    self.anime = anime_season(int(self.num)-1)
            elif self.param == 'season':
                self.anime = anime_season()
            elif self.param == "season_list":
                self.anime = anime_season_all()
            elif self.param == "anime_num":
                if self.person and self.num.isdigit():
                    if self.person in waiting_respond:
                        self.anime.append(waiting_respond[self.person][int(self.num)-1])
                        del waiting_respond[self.person]

            else:
                if not self.param.isdigit():
                    self.anime = anime_search(self.param)
        else:
            anime_json = random.choice(data)
            title = anime_json['canonicalTitle']
            anime = anime_search(title)
            if len(anime)>1:
                anime_random = random.choice(anime)
                self.anime = [anime_random]
            else:
                self.anime = anime

    def send_anime(self):
        if not self.anime:
            bot.send_message(self.instance,"*No he encontrado nada* 😢" , self.conversation)
        else:
            if self.param == 'season_list':
                text = "*Animes de Temporada*\n"
                count = 1
                for anime in self.anime:
                    text+= str(count) +". "+ anime + "\n"
                    count+=1
                text+= "*Elige un anime -> !anime temp {número}*"
                bot.send_message(self.instance,text,self.conversation)
            else:
                if len(self.anime)>1:
                    text = "*Resultados*\n"
                    count = 1
                    for anime in self.anime:
                        text += str(count) + ". " + anime['title'] + "\n"
                        count += 1
                    text += "*Elige un anime -> !anime {número}*"
                    waiting_respond[self.person] = self.anime
                    bot.send_message(self.instance, text, self.conversation)
                else:
                    text = "*"+str(self.anime[0]['title'])+"* \n*Estado*: " + str(self.anime[0]['status']) + "\n*Géneros*: " + str(self.anime[0]['genres']) + "\n*Sinopsis*: " + str(self.anime[0]['description'])
                    image_path = helper.get_image(self.anime[0]['image_url'], self.anime[0]['title'])
                    bot.send_image(self.instance, self.conversation, image_path, text)


def anime_search_mal(title):

    url = 'https://myanimelist.net/search/all?q=' + title.strip().replace(' ', '%20')
    print("URL : " + url)
    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")

    words = title.lower().split()
    animes = []

    if html.find('h2',{'id':'anime'}):
        result = html.find('h2', {'id': 'anime'}).findNext('article')
        result = result.findAll('div',{'class':'list di-t w100'})
        for anime in result:
            anime_type = anime.find('div',{'class':'pt8 fs10 lh14 fn-grey4'}).find('a').getText()
            if anime_type == "TV" or anime_type == "OVA":
                anime_title = anime.find('div',{'class':'information di-tc va-t pt4 pl8'}).find('a',{'class':'hoverinfo_trigger fw-b fl-l'}).getText()
                if len(words_in_str(words, anime_title.lower())) == len(words):
                    anime_href = anime.find('a', {'class': 'hoverinfo_trigger'})['href']
                    req = requests.get(anime_href)
                    anime_html = BeautifulSoup(req.text, "html.parser")
                    sidebar = anime_html.find('div', {'class': 'js-scrollfix-bottom'})
                    anime_description = anime_html.find('span', {'itemprop': 'description'}).getText().encode('utf8').split('.')[0]
                    anime_image = sidebar.find('img')['src']
                    anime_status = sidebar.find('span',text="Status:").parent.getText().replace('Status:','').strip().encode('utf8')

                    genres_tags = anime_html.findAll('a', attrs={'href': re.compile('/anime/genre/*')})
                    genres_out = ""
                    for genre in genres_tags:
                        genres_out += genre.getText().encode('utf8') + ", "
                    anime_genres = genres_out[:-2]

                    anime_dict = {
                        'title': anime_title.encode('utf8'),
                        'genres': anime_genres,
                        'status': anime_status,
                        'image_url': anime_image,
                        'description': anime_description
                    }
                    animes.append(anime_dict)

    return animes

def anime_search_flv(title):

    url = 'https://animeflv.net/browse?q=' + title.lower().strip().replace(' ', '+')
    print("URL : " + url)
    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")
    result = html.findAll('article', {'class': 'Anime alt B'})

    words = title.lower().split()
    animes = []

    if result:
        for anime in result:
            if anime.find('span', {'class': 'Type tv'}) or anime.find('span', {'class': 'Type ova'}):
                anime_title = anime.find('h3', {'class': 'Title'}).getText()
                if len(words_in_str(words, anime_title.lower())) == len(words):
                    anime_image = "https://animeflv.net" + anime.find('img')['src'].encode('utf8')
                    description_tag = anime.find('div', {'class': 'Description'})
                    anime_description = description_tag.findAll('p')[1].getText().encode('utf8').split('.')[0]
                    anime_href = anime.find('a')['href']
                    req = requests.get("https://animeflv.net" + anime_href)
                    html = BeautifulSoup(req.text, "html.parser")
                    result = html.find('nav', {'class': 'Nvgnrs'})
                    anime_genres = [x.getText().encode('utf8') for x in result.findAll('a')]
                    anime_status = html.find('span', {'class': 'fa-tv'}).getText().encode('utf8')
                    anime_dict = {
                        'title': anime_title.encode('utf8'),
                        'genres': ' '.join(anime_genres),
                        'image_url': anime_image,
                        'status': anime_status,
                        'description': anime_description
                    }
                    animes.append(anime_dict)

    return animes

def words_in_str(words, s):
    words = words[:]
    found = []
    for match in re.finditer('\w+', s):
        word = match.group()
        if word in words:
            found.append(word)
            words.remove(word)
            if len(words) == 0: break
    return found

def anime_search(title):

    print "Buscando anime: " + title.lower()
    print "Buscando en AnimeFLV... "
    result = anime_search_flv(title)

    if result:
        return result
    else:
        print "Buscando en MAL... "
        return anime_search_mal(title)


def anime_season_all():
    url = 'http://jkanime.net/'
    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")
    animes_temp = html.find('ul', {'class': 'latestul'}).findAll('img')

    anime_list = []
    for anime in animes_temp:
            title = anime.parent.getText().encode('utf8')
            anime_list.append(title)
    return anime_list


def anime_season(num=None):
    url = 'http://jkanime.net/'
    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")

    animes_temp = html.find('ul',{'class':'latestul'}).findAll('img')

    if num:
        anime_href = animes_temp[num].parent['href']
    else:
        anime  = random.choice(animes_temp)
        anime_href = anime.parent['href']

    req = requests.get(anime_href)
    anime = BeautifulSoup(req.text, "html.parser")

    anime_title = anime.find('div', {'class': 'sinopsis_title title21'}).getText().encode('utf8')
    anime_description = anime.find('div', {'class': 'sinoptext'}).find('p').getText().encode('utf8').split('.')[0]
    image_url = anime.find('div', {'class': 'separedescrip'}).find('img')['src']
    anime_genres = [x.getText().encode('utf8') for x in anime.findAll('a', {'style': 'color:#09F; text-decoration:none;'})]

    return [{
        'title': anime_title,
        'genres': ' '.join(anime_genres),
        'description': anime_description,
        'status': 'En emision',
        'image_url': image_url
    }]