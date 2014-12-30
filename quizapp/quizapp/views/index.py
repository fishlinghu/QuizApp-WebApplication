#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.question import Question
from quizapp.models.player import Player
from quizapp.models.topic import Topic 
from google.appengine.ext import db

class IndexHandler(Handler):
    topics = Topic.all()
    def render_homepage(self, **kw):
        if (self.check_clearance()):
            self.render("index.html", **kw)

    def get(self):
        playerID = self.session['QUIZAPP_USER']
        player = Player.get_by_id(playerID)  
        self.response.headers['Content-Type'] = 'text/html'
        self.render_homepage(name = player.account, topics=self.topics)
