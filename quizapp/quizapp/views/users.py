#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from quizapp.models.player import Player
from views import Handler

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
        
        #Check if player exists in the datastore
        player = checkPlayer(username)
        
        if player :
            if player.password == password:
                self.session['QUIZAPP_USER'] = player.key().id()
                self.redirect('index')
            else :
                self.render("homepage.html", error="Invalid username or password", error_type="alert-danger")
        else :
            self.render("homepage.html", error="Invalid username or password", error_type="alert-danger")
        
class LogoutHandler(Handler):
    def get(self):
        self.session.pop('QUIZAPP_USER')
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
                self.render("homepage.html", error="Username is already in use. Please use a different username", error_type="alert-danger")
            else:
                #Create new Player object
                player = Player(account = username,
                                password = password,
                                name = displayName)
                player.put()
                self.redirect('/')
        else:
            self.render("homepage.html", error="Passwords do not match. Please try again", error_type="alert-danger")