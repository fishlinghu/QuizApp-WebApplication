#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from webapp2_extras import security
from quizapp.models.player import Player
from views import Handler

secretPepper = """
VyPYorPdj45z43ZG
doNZSGBev1iaLx72
byGvGGOpaw6lUwiD
pyQtV0mIHPybSX89
XjmeVqJsfsDEGxqA
AvHzw6Xx4nTs585k
zjM4MLKr2FLSrLU3
jlnhMc9RENEndPwc
"""


def checkPlayer(username):
    #Query Datastore for player
    q = db.Query(Player)
    q.filter('account =', username)
    results = q.get()
        
    #Check if no such player exists
    if not results:
        return None
    else :
        return results

class LoginHandler(Handler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        if password:
            password = security.hash_password(password, method='sha512', pepper=secretPepper)
        
        #Check if player exists in the datastore
        player = checkPlayer(username)
        
        if player :
            if player.password == password:
                self.session['QUIZAPP_USER'] = player.key().id()
                self.redirect('index')
            else :
                self.render("homepage.html", message="Invalid username or password", message_type="alert-danger")
        else :
            self.render("homepage.html", message="Invalid username or password", message_type="alert-danger")
        
class LogoutHandler(Handler):
    def get(self):
        self.session.pop('QUIZAPP_USER')
        if 'QUIZAPP_QUIZ' in self.session:
            self.session.pop('QUIZAPP_QUIZ')
        self.redirect('/')       
        
class RegisterHandler(Handler):
    def post(self):
        username = self.request.get('username')
        displayName = self.request.get('displayName')
        password = self.request.get('password')
        password2 = self.request.get('password2')
        
        #Check if passwords match
        if password == password2 :
            #Check if username is already in use
            player = checkPlayer(username)
        
            if player:
                self.render("homepage.html", message="Username is already in use. Please use a different username", message_type="alert-danger")
            else:
                #Create new Player object
                player = Player(account = username,
                                password = security.hash_password(password, method='sha512', pepper=secretPepper),
                                name = displayName,
                                intro = None,
                                level = 1,
                                experience = 0
                                )
                player.put()
                self.session['QUIZAPP_USER'] = player.key().id()
                self.redirect('index')
        else:
            self.render("homepage.html", message="Passwords do not match. Please try again", message_type="alert-danger")