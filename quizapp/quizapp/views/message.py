#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.message import Message
from quizapp.models.player import Player
from datetime import datetime

class MessageHandler(Handler):
    def render_homepage(self, **kw):
        self.render("message.html", **kw)

    def get(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            # Get the player
            player = Player.get_by_id(user)

            # Get friends list, I think we should show the friend list in this page
            # So the player can send message to their friends
            # Maybe we can use some fancy ways to implement this function
            # But this version I'll just get the names of friends
            friend_name_list = []
            for friend_ID in player.friend_list:
                friend = Player.get_by_id(friend_ID)
                friend_name_list.append(friend.name)

            # Get all inbox message, ordered as the newest first 
            q = Message.all()
            q.filter('receiver_ID = ', user).order('-create_time')
            in_message_list = q

            # Get all sent message, ordered as the newest first 
            q = Message.all()
            q.filter('sender_ID = ', user).order('-create_time')
            sent_message_list = q

            # Get the list of inbox messages' topics and contents 
            in_message_topic_list = []
            in_message_content_list = []
            in_message_time_list = []
            sender_name_list = []
            # Here might be a BUG
            # I am not sure whether content (TextProperty) can be saved in a list
            for in_message in in_message_list:
                in_message_topic_list.append(in_message.topic)
                in_message_content_list.append(in_message.content)
                in_message_time_list.append(in_message.create_time)
                sender = Player.get_by_id(in_message.sender_ID)
                sender_name_list.append(sender.name)

            # Get the list of sent messages' topics and contents 
            sent_message_topic_list = []
            sent_message_content_list = []
            sent_message_time_list = []
            receiver_name_list = []
            # Here might be a BUG
            # I am not sure whether content (TextProperty) can be saved in a list
            for sent_message in sent_message_list:
                sent_message_topic_list.append(sent_message.topic)
                sent_message_content_list.append(sent_message.content)
                sent_message_time_list.append(sent_message.create_time)
                receiver = Player.get_by_id(sent_message.receiver_ID)
                receiver_name_list.append(receiver.name)

            template_values = {
                               'name' : player.account,
                               'friend_name_list': friend_name_list,
                               'receiver_name_list': receiver_name_list,
                               'sent_message_topic_list': sent_message_topic_list,
                               'sent_message_content_list': sent_message_content_list,
                               'sent_message_time_list': sent_message_time_list,
                               'sender_name_list': sender_name_list,
                               'in_message_topic_list': in_message_topic_list,
                               'in_message_content_list': in_message_content_list,
                               'in_message_time_list': in_message_time_list
                               }

            self.render("message.html", **template_values)
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.render_homepage()
    def post(self):
        # In case you want to send a message to other player
        user = self.session.get('QUIZAPP_USER')
        if user:
            receiver_name = self.request.get('receiver_name')
            q = Player.all()
            q.filter('name = ', receiver_name)
            receiver = q.get()
            if receiver:
                topic = self.request.get('topic')
                content = self.request.get('content')
                # Need to assign the message ID, or just use key?
                new_message = Message(
                    topic = topic,
                    content = content, 
                    receiver_ID = receiver.key().id(),
                    sender_ID = user,
                    create_time = datetime.now())
                new_message.put()
                self.redirect('/message')
            else:
                # No such player
                self.write_plain('The player does not exist')

        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.render_homepage()
