import requests
from bs4 import BeautifulSoup
from app.bot import bot


class Chiste(object):
    def __init__(self, instance, conversation):
        self.instance = instance
        self.conversation = conversation
        self.chiste = ''
        self.build()

    def build(self):
        url = 'http://pagina-del-dia.euroresidentes.es/chiste-del-dia/gadget-chiste-del-dia.php?modo=2'
        req = requests.get(url)
        html = BeautifulSoup(req.text, "html.parser")
        self.chiste = html.find('td', {'bgcolor': '#FFFFFF'}).getText()

    def send_chiste(self):
        bot.send_message(self.instance, "*" + self.chiste + "*", self.conversation)