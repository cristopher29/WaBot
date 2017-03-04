#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.utils import helper
from app.receiver.receiver import Receiver
from app.receiver import receiver
from app.bot import bot
from app.quedada.voter import Voter


class Quedada(Receiver):
    def __init__(self, instance, conversation, creator, title, identifier="👍"):
        # Finish poll if user already has one in this conversation
        finish_quedada(instance, creator, conversation)
        Receiver.__init__(self, identifier, conversation, creator, self.handle_answer)
        self.instance = instance
        self.title = title
        self.voters = []

    def handle_answer(self, message_entity=None):
        if message_entity is not None:
            voter = Voter(message_entity)
            if not any(voter.who == v.who for v in self.voters):
                self.voters.append(voter)
            print("Got vote")

    def send_quedada(self):
        answer = "Próxima quedada: *" + self.title + "*" + "\n" + self.identifier + " para asistir"
        bot.send_message(self.instance, answer, self.conversation)

    def is_creator(self, creator):
        return self.creator == creator

    def is_conversation(self, conversation):
        return self.conversation == conversation

    def voters_string(self):
        answer = ""
        for voter in self.voters:
            answer += "\n+ " + voter.who_name

        return answer


def finish_quedada(self, creator, conversation):
    quedada = quedada_from_user_conversation(creator, conversation)
    if quedada:
        message = "*Quedada " + quedada.title + ":*\n"
        message += "Asistencia total: " + str(len(quedada.voters))
        message += quedada.voters_string()
        bot.send_message(self, message, quedada.conversation)
        quedada.destroy()


def quedada_from_user_conversation(creator, conversation):
    for quedada in receiver.receivers:
        if is_quedada(quedada):
            if quedada.is_creator(creator):
                if quedada.is_conversation(conversation):
                    return quedada

    return None


def user_has_quedada(creator, conversation):
    for quedada in receiver.receivers:
        if quedada.is_creator(creator):
            if quedada.is_conversation(conversation):
                return True

    return False


def is_quedada(obj):
    return type(obj) is Quedada