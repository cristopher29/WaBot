#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string, requests, os
from app.bot import bot
from app.utils import helper
from app.yesno.yesno import YesNo
from app.anime.anime import Anime
from app.webs.quote.quote import Quote
from app.passwords import CLEVER_API_KEY
from app.clever.clever import Cleverbot
from app.webs.adv.adv import ADV
from app.webs.noticias.noticias import Noticias
from app.webs.chiste.chiste import Chiste
from app.webs.wur.wur import WUR
from app.webs.chollo.chollo import Chollo


def handle_message(instance, command, predicate, message_entity, who, conversation):
    if command == "hola":
        who_name = helper.sender_name(message_entity)
        bot.send_message(instance, "Hola *"+ who_name +"*".decode('utf8'), conversation)

    elif command == "ayuda":

        answer = """*Lista de comandos*\n
                 !hola\n
                 !noticia <videojuegos,ciencia,series,música,actualidad>\n
                 !chollo\n
                 !anime <temp, temp lista, búsqueda>\n
                 !adv\n
                 !chiste\n
                 !siono \n
                 !ayuda"""

        bot.send_message(instance, answer, conversation)

    elif command == "siono":
        yesno = YesNo(instance, conversation)
        yesno.send_yesno()

    elif command == "anime":
        anime = None
        person = helper.get_who_send(message_entity)
        if predicate:
            if predicate == "temp":
                anime = Anime(instance, conversation, person, param='season')
            elif predicate == "temp lista":
                anime = Anime(instance, conversation, person, param='season_list')
            elif predicate.isdigit():
                anime = Anime(instance, conversation, person, param='anime_num', num=predicate)
            else:
                commands = predicate.split()
                if len(commands)==2 and commands[0] == "temp" and commands[1].isdigit():
                    anime = Anime(instance, conversation, person, param='season_num', num=commands[1])
                # Buscar anime
                else:
                    anime = Anime(instance, conversation, person, param=predicate)
        else:
            #Anime aleatorio
            anime = Anime(instance, conversation, person)

        if(anime):
            anime.send_anime()

    elif command == "chollo":
        chollo = Chollo(instance, conversation)
        chollo.build()
        chollo.send_chollo()

    # elif command == "frase":
    #     quote = Quote(instance, conversation)
    #     quote.send_quote()

    elif command == "chiste":
        chiste = Chiste(instance, conversation)
        chiste.send_chiste()

    # elif command == "wur":
    #     wur = WUR(instance, conversation)
    #     wur.build()
    #     wur.send_wur()

    elif command == "adv":
        adv = ADV(instance, conversation)
        adv.send_adv()

    elif command == "noticia":
        l = ['videojuegos', 'ciencia', 'series','música', 'actualidad']
        if predicate.encode('utf8') in l:
            noticia = Noticias(instance, conversation, predicate)
            noticia.send_noticia()

    #cambia la foto del perfil
    elif command == "fotoPerfil":
        path = get_avatar()
        bot.profile_set_picture(instance, path)

    #cambia el estado del perfil
    elif command == "estado":
        if predicate:
            bot.profile_setStatus(instance, predicate)

    else:
        #return
        answer = cleverbot_answer(command + " " + predicate)
        bot.send_message(instance, answer, conversation)


def get_avatar():
    path = "app/assets/images/avatar.jpg"
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'wb') as file:
        file.write(requests.get('http://lorempixel.com/640/640/cats/').content)
    return path

def cleverbot_answer(message):
    cb = Cleverbot(CLEVER_API_KEY)
    answer = cb.ask(message)
    return answer
