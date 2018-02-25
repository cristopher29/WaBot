# -*- coding: utf-8 -*-

from yowsup.layers.protocol_messages.protocolentities import *
import string, shutil, requests, re
from yowsup.common.tools import Jid

log_file = "botlog.txt"

def get_image(url, caption):
    regex = re.compile('[^0-9a-zA-Z]')
    name = regex.sub("", caption)
    path = "app/assets/images/" + name + ".jpg"
    response = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    del response
    return path

def clean_text(anime_title):
    regex = re.compile('[^0-9a-zA-ZÀ-ÿ]')
    title = regex.sub("", anime_title)
    return title.strip()

def get_who_send(message_entity):
    who = message_entity.getFrom()
    if message_entity.isGroupMessage():
        who = message_entity.getParticipant()
        
    return who
    
    
def sender_name(message_entity):
    name = message_entity.getNotify()
    return name.decode('utf8')


def get_conversation(message_entity):
    return message_entity.getFrom()

"""
Detects if the message entity is text type.
"""
def is_text_message(message_entity):
    return message_entity.getType() == "text"

"""
Detects if the message entity is media type.
Available media types:
    + image
    + location
    + vcard
"""
def is_media_message(message_entity):
    return message_entity.getType() == "media"


"""
Detects if the message entity is media -> image type
"""
def is_image_media(message_entity):
    if is_media_message(message_entity):
        return message_entity.getMediaType() == "image"


"""
Detects if the message entity is media -> image type
"""
def is_location_media(message_entity):
    if is_media_message(message_entity):
        return message_entity.getMediaType() == "location"


"""
Detects if the message entity is media -> image type
"""
def is_vcard_media(message_entity):
    if is_media_message(message_entity):
        return message_entity.getMediaType() == "vcard"


"""
Builds a sendable whatsapp message (self.toLower(message))
"""
def make_message(msg, conversation):
    outgoing_message_enity = TextMessageProtocolEntity(msg, to=Jid.normalize(conversation))
    return outgoing_message_enity


"""
Logs message to a txt file (maclog.txt, defined above of this class)
"""
def log_mac(message_entity):
    # Nigga who send the message (first name)
    who = who = sender_name(message_entity)

    # Conversation
    conversation = message_entity.getFrom()

    # Message
    message = message_entity.getBody()
    message = message.strip()
    message = ''.join(filter(lambda x: x in string.printable, message))
    message = message.strip()
    
    dirty = message_entity.getBody().strip()

    # Warn
    print("logging something...")

    # Log
    file = open(log_file, "a")
    file.write(
        "------------------------" +
        "\n" + "Sender:" + "\n" + who + "\n" + "Number sender:" + "\n" + conversation +
        "\n" + "Real msg:" + "\n" + dirty + "\n" +
        "\n" + "Clean msg:" + "\n" + message + "\n" +
        "------------------------" + "\n" + "\n")
    file.close()


"""
Returns predicate of the message
"""
def predicate(message):
    message = clean_message(message)
    if is_shorcut(message):
        return message[1:]
    else:
        return message


"""
Cleans all the garbage and non-ASCII characters in the message (idk why whatsapp appends all that garbage)
"""
def clean_message(message_entity):
    message = message_entity.getBody()
    message = message.strip()
    #message = ''.join(filter(lambda x: x in string.printable, message))
    return message


"""
Detects if the message is a command for Mac
"""
def is_command(message_entity):
    message = clean_message(message_entity)
    return is_shorcut(message) and len(message) > 1

def is_shorcut(message):
    macShorcut = message[:1]
    return macShorcut == "!"


"""
Converts a list into a comma separated string
"""
def nice_list(list):
    return "[" + ", ".join( str(x) for x in list) + "]"
    
