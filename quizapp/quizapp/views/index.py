#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.question import Question
from quizapp.models.player import Player
from quizapp.models.topic import Topic 
from google.appengine.ext import db

class IndexHandler(Handler):
    def render_index(self, **kw):
        if (self.check_clearance()):
            self.render("index.html", **kw)

    def get(self):
        topics = Topic.all()
        playerID = self.session['QUIZAPP_USER']
        player = Player.get_by_id(playerID)  
        self.response.headers['Content-Type'] = 'text/html'
        quiz_key = self.session.get('QUIZAPP_QUIZ')
        waiting = self.session.get('QUIZAPP_FINISHED')
        
        if quiz_key:
            self.session['QUIZAPP_QUIZ'] = None
        
        if waiting:
            self.session['QUIZAPP_FINISHED'] = None
            
        self.render_index(name = player.account, topics = topics)
