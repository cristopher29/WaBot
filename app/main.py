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
from app.quedada import quedada
from app.webs.youtube.youtube import Youtube
from app.webs.adv.adv import ADV
from app.webs.noticias.noticias import Noticias
from app.webs.chiste.chiste import Chiste

####################################################################################################################


def handle_message(instance, command, predicate, message_entity, who, conversation):

    if command == "hola":
        who_name = helper.sender_name(message_entity)
        answer = "Hola *" + who_name + "*"
        bot.send_message(instance, answer, conversation)

    elif command == "newmember":
        answer = "🎊 *Bienvenido al grupo!* 🎊".decode('utf8')
        bot.send_message(instance, answer, conversation)

    elif command == "ayuda":

        # "\n!anime <búsqueda>" \
        # "\n!anime season" \
        # "\n!youtube <búsqueda>" \

        answer = "*Lista de comandos* " \
                 "\n!hola" \
                 "\n!noticia <games,ciencia,series,música,actualidad>" \
                 "\n!adv " \
                 "\n!frase" \
                 "\n!chiste" \
                 "\n!siono" \
                 "\n!ayuda".decode('utf8')

        bot.send_message(instance, answer, conversation)

    elif command == "siono":
        yesno = YesNo(instance, conversation)
        yesno.send_yesno()

    # elif command == "anime":
    #     if predicate:
    #         if predicate == 'season':
    #             anime = Anime(instance, conversation, param='season')
    #         else:
    #             anime = Anime(instance, conversation, param=predicate)
    #     else:
    #         anime = Anime(instance, conversation)
    #
    #     anime.send_anime()

    elif command == "frase":
        quote = Quote(instance, conversation)
        quote.send_quote()

    elif command == "chiste":
        chiste = Chiste(instance, conversation)
        chiste.send_chiste()

    # elif command == "youtube":
    #     if predicate:
    #         youtube = Youtube(instance, conversation, predicate)
    #         youtube.send_youtube()

    elif command == "adv":
        adv = ADV(instance, conversation)
        adv.send_adv()

    elif command == "noticia":

        l = ['games', 'ciencia', 'series','música'.decode('utf8'), 'actualidad']
        if predicate in l:
            noticia = Noticias(instance, conversation, predicate)
            noticia.send_noticia()


    elif command == "quedada":

        if predicate:
            if predicate == "finalizar":
                quedada.finish_quedada(instance, who, conversation)
                return
            else:
                lugar = predicate
                new_quedada = quedada.Quedada(instance, conversation, who, lugar)
                new_quedada.send_quedada()
        else:
            bot.send_message(instance, "Establece un lugar", conversation)
            return

    #cambia la foto del perfil
    elif command == "fotoPerfil":
        path = get_image()
        bot.profile_setPicture(instance, path)

    #cambia el estado del perfil
    elif command == "estado":
        if predicate:
            bot.profile_setStatus(instance, predicate)

    else:
        #return
        answer = cleverbot_answer(command + " " + predicate)
        bot.send_message(instance, answer, conversation)


def get_image():
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
