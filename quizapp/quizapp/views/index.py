#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.question import Question
from quizapp.models.player import Player
from google.appengine.ext import db

class IndexHandler(Handler):
    def render_homepage(self, **kw):
        self.render("index.html", **kw)

    def get(self):
        playerID = self.session['QUIZAPP_USER']
        player = Player.get_by_id(playerID)  
        self.response.headers['Content-Type'] = 'text/html'
        self.render_homepage(name = player.account)
        """
        question1 = Question(
                            question_ID = 1,
                            description = "From what is the liqueur kirsch made?",
                            correct_ans = "cherries",
                            wrong_ans = ["lemon", "kiwi", "banana", "grapes"],
                            wiki_link = "https://en.wikipedia.org/wiki/Cherry",
                            topic = "alcohol",
                            topic_ID = 1
                            )
        question1.put()
        question2 = Question(
                            question_ID = 2,
                            description = "From which plant is tequila derived?",
                            correct_ans = "cactus",
                            wrong_ans = ["bamboo", "daisy", "orchid", "peony"],
                            wiki_link = "https://en.wikipedia.org/wiki/Cactus",
                            topic = "alcohol",
                            topic_ID = 1
                            )
        question2.put()
        question3 = Question(
                            question_ID = 3,
                            description = "Which drug kills more people below the age of 21 than any other?",
                            correct_ans = "alcohol",
                            wrong_ans = ["cocaine", "marijuana", "nicotine", "nurofen"],
                            wiki_link = "https://en.wikipedia.org/wiki/Alcohol",
                            topic = "alcohol",
                            topic_ID = 1
                            )
        question3.put()
        """
