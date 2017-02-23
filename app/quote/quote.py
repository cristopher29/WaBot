import requests
from app.bot import bot

api_url = "http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"


class Quote(object):
    def __init__(self, instance, conversation):
        self.instance = instance
        self.conversation = conversation
        self.quote = ""
        self.autor = ""
        self.build()

    def build(self):
        response = requests.get(api_url)
        data = response.json()
        self.quote = data["quoteText"].strip()
        self.autor = data["quoteAuthor"]

    def send_quote(self):
        bot.send_message(self.instance, "*" + self.quote + "* \n -" + self.autor, self.conversation)
