#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.bot import bot
import json, random, requests, xmltodict, re
from collections import OrderedDict

with open('app/assets/json/anime.json') as data_file:
    data = json.load(data_file)

class Anime(object):
    def __init__(self, instance, conversation):
        self.instance = instance
        self.conversation = conversation
        self.title = ""
        self.genre = ""
        self.epis = ""
        self.image_path = ""
        self.no_anime = False
        self.build()

    def build(self):
        anime = random.choice(data)
        anime_lower = anime['canonicalTitle'].lower().replace(" ", "_")
        anime_lower = re.sub(r"/!^;.:¿¡","",anime_lower)
        api = requests.get('https://myanimelist.net/api/anime/search.xml?q=' + anime_lower,auth=('', ''))
        if api.status_code != 204:
		
            xml_dict = xmltodict.parse(api.content)
            input_dict  = OrderedDict(xml_dict)
            output_dict = json.loads(json.dumps(input_dict))
            if type(output_dict['anime']['entry']) is list:
                self.image_path = get_image(output_dict['anime']['entry'][0]['image'], anime_lower)
            else:
                self.image_path = get_image(output_dict['anime']['entry']['image'], anime_lower)

            self.title = anime['canonicalTitle']
            self.epis = str(anime['totalEpisodes'])
            self.genre = ", ".join(str(x) for x in anime['genres'])
        else:
            self.no_anime = True

    def send_anime(self):
        # Converts gif to mp4 and sends as video
        # bot.send_video(self.instance, self.conversation, gif_to_video(self.image_path, self.caption), self.caption)

        # Sends gif as image
        if self.no_anime:
            bot.send_message(self.instance,"*No he encontrado nada* :(" , self.conversation)
        else:
            text = u"*"+self.title+"* \n*Episodios*: " + self.epis + "\n*Géneros*: " + self.genre
            bot.send_image(self.instance, self.conversation, self.image_path, text)
            # Sends just the answer
        


def get_image(url, caption):
    path = "app/assets/images/" + caption + ".jpg"
    file = open(path, 'wb')
    file.write(requests.get(url).content)
    file.close()
    return path
