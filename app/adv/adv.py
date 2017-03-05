import requests, random
from app.bot import bot
from bs4 import BeautifulSoup

class ADV(object):
    def __init__(self, instance, conversation):
        self.instance = instance
        self.conversation = conversation
        self.adv = ""
        self.build()

    def build(self):
        self.adv = get_adv()

    def send_adv(self):
        bot.send_message(self.instance, "*" + self.adv + "*", self.conversation)

def get_adv():

    url = 'http://www.ascodevida.com/aleatorio'

    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")

    advs = html.find_all('div', {'class':'box story'})

    return advs[0].find('p').find('a').getText().strip()