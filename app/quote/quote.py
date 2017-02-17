import requests
import moviepy.editor as mp
from app.bot import bot
import json

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
        #self.image_path = get_image(json["image"], self.caption)

    def send_quote(self):
        # Converts gif to mp4 and sends as video
        # bot.send_video(self.instance, self.conversation, gif_to_video(self.image_path, self.caption), self.caption)

        # Sends gif as image
        # bot.send_image(self.instance, self.conversation, self.image_path, self.caption)

        # Sends just the answer
        bot.send_message(self.instance, "*" + self.quote + "* \n -" + self.autor, self.conversation)
