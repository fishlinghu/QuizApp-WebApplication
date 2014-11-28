#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from quizapp.models.player import Player
from views import Handler

class LoginHandler(Handler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
class LogoutHandler(Handler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'        
        
class RegisterHandler(Handler):
    def post(self):
        username = self.request.get('username')
        displayName = self.request.get('displayName')
        password = self.request.get('password')
        password2 = self.request.get('password2')
        
        player = Player(key_name = 1,
                        account = username,
                        password = password,
                        name = displayName)
        player.put()
        self.redirect('/')