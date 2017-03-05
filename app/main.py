#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from app.bot import bot
from app.utils import helper
from app.yesno.yesno import YesNo
from app.anime.anime import Anime
from app.quote.quote import Quote
from app.passwords import CLEVER_API_KEY
from app.clever.clever import Cleverbot
from app.quedada import quedada
from app.youtube.youtube import Youtube
from app.adv.adv import ADV
from app.noticias.noticias import Noticias

####################################################################################################################


def handle_message(instance, command, predicate, message_entity, who, conversation):

    if command == "hola":
        who_name = helper.sender_name(message_entity)
        answer = "Hola *" + who_name + "*"
        bot.send_message(instance, "Hola", conversation)

    elif command == "newmember":
        answer = "🎊 *Bienvenido al grupo!* 🎊".decode('utf-8')
        bot.send_message(instance, answer, conversation)

    elif command == "ayuda":

        answer = "*Lista de comandos* " \
                 "\n!hola " \
                 "\n!anime <búsqueda> " \
                 "\n!anime season " \
                 "\n!youtube <búsqueda> " \
                 "\n!noticia <anime,games,ciencia,series,música,actualidad> " \
                 "\n!adv " \
                 "\n!quote " \
                 "\n!siono " \
                 "\n!ayuda".decode('utf-8')

        bot.send_message(instance, answer, conversation)

    elif command == "siono":
        yesno = YesNo(instance, conversation)
        yesno.send_yesno()

    elif command == "anime":
        if predicate:
            if predicate == 'season':
                anime = Anime(instance, conversation, param='season')
            else:
                anime = Anime(instance, conversation, param=predicate)
        else:
            anime = Anime(instance, conversation)

        anime.send_anime()

    elif command == "quote":
        quote = Quote(instance, conversation)
        quote.send_quote()

    elif command == "youtube":
        if predicate:
            youtube = Youtube(instance, conversation, predicate)
            youtube.send_youtube()

    elif command == "adv":
        adv = ADV(instance, conversation)
        adv.send_adv()

    elif command == "noticia":

        l = ['games', 'ciencia', 'series','música', 'actualidad','anime']
        if predicate in l:
            if predicate == 'anime':
                noticia = Noticias(instance, conversation, predicate)
                noticia.send_noticia_anime()
            else:
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

    else:
        return
        #answer = cleverbot_answer(command + " " + predicate)
        #bot.send_message(instance, answer, conversation)


def cleverbot_answer(message):
    cb = Cleverbot(CLEVER_API_KEY)
    answer = cb.ask(message)
    return answer.decode('utf-8')
