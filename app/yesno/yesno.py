import random
from app.bot import bot

class YesNo(object):
    def __init__(self, instance, conversation):
        self.instance = instance
        self.conversation = conversation
        self.siono = ""
        self.build()

    def build(self):
        sino = ['Si','No']
        self.siono = random.choice(sino)

    def send_yesno(self):
        bot.send_message(self.instance, "*" + self.siono + "*", self.conversation)
