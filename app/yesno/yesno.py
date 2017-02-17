import requests, random
import moviepy.editor as mp
from app.bot import bot

api_url = "https://yesno.wtf/api/"


class YesNo(object):
    def __init__(self, instance, conversation):
        self.instance = instance
        self.conversation = conversation
        self.caption = ""
        self.image_path = ""
        self.build()

    def build(self):
        siono = ['Si','No']
        response = random.choice(siono)
        self.caption = response
        #self.image_path = get_image(json["image"], self.caption)

    def send_yesno(self):
        # Converts gif to mp4 and sends as video
        # bot.send_video(self.instance, self.conversation, gif_to_video(self.image_path, self.caption), self.caption)

        # Sends gif as image
        # bot.send_image(self.instance, self.conversation, self.image_path, self.caption)

        # Sends just the answer
        bot.send_message(self.instance, "*" + self.caption + "*", self.conversation)


'''
Converts gif to video (mp4)
return video file path
'''


def gif_to_video(image_path, caption):
    path = "app/assets/images/" + caption + ".mp4"
    clip = mp.VideoFileClip(image_path)
    clip.write_videofile(path)
    return path


'''
Downloads image from url
returns image file path
'''


def get_image(url, caption):
    path = "app/assets/images/" + caption + ".gif"
    file = open(path, 'wb')
    file.write(requests.get(url).content)
    file.close()
    return path


def translate_caption(caption):
    if caption == "yes":
        return "Si"
    else:
        return "No"
