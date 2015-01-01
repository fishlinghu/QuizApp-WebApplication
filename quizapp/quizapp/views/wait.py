#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import random
import json
import logging
from google.appengine.ext import db
from quizapp.models.game import Game
from quizapp.models.question import Question
from quizapp.models.player import Player
from quizapp.models.topic import Topic
from google.appengine.api import channel

class WaitHandler(Handler):
    def render_wait(self, **kw):
        self.render("wait.html", **kw)

    def get(self, topic):
        self.response.headers['Content-Type'] = 'text/html'
        user = self.session.get('QUIZAPP_USER')
        quiz_key = self.session.get('QUIZAPP_QUIZ')
        
        q = db.Query(Topic)
        q.filter('topicID =', topic)
        topicID = q.get().key().id()
        
        if user:
            playerID = self.session['QUIZAPP_USER']
            player = Player.get_by_id(playerID)
            if not quiz_key:
                q = db.Query(Game)
                q.filter('b_ID =', None)
                q.filter('a_ID !=', user)
                q.filter('topic_ID =', topicID) 
                quiz = q.get()
                
                if not quiz:
                    q = db.Query(Question)
                    q.filter('topic_ID =', topicID)
        
                    questionRange = q.count()
                    questions = []
                    
                    for i in range(5):
                        #Generate a random integer which dictates the question at that position
                        questionNumber = random.randint(0, questionRange - 1)
                        #Get the question from the datastore using the randomly generated integer
                        question = q.get(offset = questionNumber)
                        #Append question ID
                        questions.append(question.key().id())
                        
                    quiz = Game(
                                a_ID = user,
                                question_set = questions,
                                a_ans_list = [],
                                b_ans_list = [],
                                a_score = 0,
                                b_score = 0,
                                a_score_list = [],
                                b_score_list = [],
                                topic_ID = topicID
                                )
                    quiz.put()
                    quiz_key = quiz.key().id()
                    self.session['QUIZAPP_QUIZ'] = quiz_key
                    self.render_wait(name = player.account, topic = topic)
                else:
                    quiz.b_ID = user
                    quiz.put()
                    quiz_key = quiz.key().id()
                    self.session['QUIZAPP_QUIZ'] = quiz_key
                    self.redirect("/quiz/" + topic + "/")
            else:
                quiz = Game.get_by_id(int(quiz_key))
                opponant = quiz.b_ID
                if not opponant:
                    self.render_wait(name = player.account, topic = topic)
                else:
                    self.redirect("/quiz/" + topic + "/")
        else:
            self.redirect('/')