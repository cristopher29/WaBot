#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import time
import random

from app import main
from app.utils import helper
from app.bot import bot
from app.receiver import receiver

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_contacts.protocolentities import *
from yowsup.layers.protocol_groups.protocolentities import *
from yowsup.layers.protocol_groups.protocolentities.notification_groups_add import AddGroupsNotificationProtocolEntity

allowedPersons=['34695529542-1487091202','34695529542-1417819580']
ap = set(allowedPersons)

'''
Basic flow. DO NOT TOUCH
Modifying this block automatically makes you a piece of shit
####################################################################################################################
####################################################################################################################
'''
class BotLayer(YowInterfaceLayer):
    PROP_CONTACTS = "org.openwhatsapp.yowsup.prop.syncdemo.contacts"

    def __init__(self):
        super(BotLayer, self).__init__()

    # Callback function when there is a successful connection to Whatsapp server
    @ProtocolEntityCallback("success")
    def on_success(self, success_entity):
        contacts = self.getProp(self.__class__.PROP_CONTACTS, [])
        print("Sync contacts sucess: " + helper.nice_list(contacts))
        contact_entity = GetSyncIqProtocolEntity(contacts)
        self._sendIq(contact_entity, self.on_sync_result, self.on_sync_error)

    @ProtocolEntityCallback("notification")
    def onNotification(self, notification):
        """
            Reacts to any notification received
        """
        self.toLower(notification.ack())

        if isinstance(notification, AddGroupsNotificationProtocolEntity):  # added new member
            conver = notification.getFrom()
            main.handle_message(self, "newmember", "", notification , "", conver)

    def on_sync_result(self,
                       result_sync_iq_entity,
                       original_iq_entity):
        print("Sync result:")
        print(result_sync_iq_entity)

    def on_sync_error(self,
                      error_sync_iq_entity,
                      original_iq_entity):
        print("Sync error:")
        print(error_sync_iq_entity)


    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        self.toLower(entity.ack())
        #print(entity.ack())


    @ProtocolEntityCallback("message")
    def on_message(self, message_entity):
        if helper.is_text_message(message_entity):
            print (message_entity.getFrom(False) + " : " + message_entity.getBody().encode('utf-8'))

            # Set received (double v) and add to ack queue
            bot.receive_message(self, message_entity)

            # Handle intercepts if needed
            receiver.intercept(self, message_entity)

            #if message_entity.getFrom(False) in ap:
            # If is a bot order. (Message starts with '!')
            if bot.should_write(message_entity):
                # Prepare bot to answer (Human behavior)
                bot.prepate_answer(self, message_entity)

                # Send the answer, here magic happens
                self.on_text_message(message_entity)
                #time.sleep(random.uniform(0.5, 1.5))

            # Finally Set offline
            bot.disconnect(self)

    def on_text_message(self, message_entity):
        # Detect command and the predicate of the message
        command = ""
        predicate = ""

        try:
            command = helper.predicate(message_entity).split(' ', 1)[0]
            predicate = helper.predicate(message_entity).split(' ', 1)[1]
        except IndexError:
            print("No predicate")
        # Log
        # helper.log_mac(message_entity)
        who = helper.get_who_send(message_entity)
        conversation = message_entity.getFrom()

        if helper.is_command(message_entity):
            main.handle_message(self, command, predicate, message_entity, who, conversation)

'''
Just ignore everything above (this block)
Modifying this block automatically makes you a piece of shit
####################################################################################################################
####################################################################################################################
'''
