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

class QuizHandler(Handler):
    def render_quiz(self, **kw):
        self.render("quiz.html", **kw)

    def get(self, topic):
        self.response.headers['Content-Type'] = 'text/html'
        user = self.session.get('QUIZAPP_USER')
        quiz_key = self.session.get('QUIZAPP_QUIZ')
        
        q = db.Query(Topic)
        q.filter('topicID =', topic)
        topicID = q.get().key().id()
        
        if user:
            quiz = Game.get_by_id(int(quiz_key))             
            
            if quiz:
                token = channel.create_channel(str(user) + str(quiz_key))
                
                question = quiz.question_set[0]
                question = Question.get_by_id(question)
                
                player1 = Player.get_by_id(quiz.a_ID)
                player2 = None
                if quiz.b_ID:
                    player2 = Player.get_by_id(quiz.b_ID)
                
                if (player1.key().id() == user):
                    player = player1
                    if player2:
                        opponent = player2
                    else :
                        opponent = None
                else:
                    player = player2
                    opponent = player1
                
                template_values = {
                    'token': token,
                    'user' : user,
                    'name': player.account,
                    'opponentName' : '' if not opponent else opponent.account,
                    'opponentLevel' : '' if not opponent else opponent.level,
                    'quiz_key': quiz_key,
                    'question': question.question,
                    'answer1' : question.correct_ans.title(),
                    'answer2' : question.wrong_ans[0].title(),
                    'answer3' : question.wrong_ans[1].title(),
                    'answer4' : question.wrong_ans[2].title(),
                    'img_link' : question.img_link
                }
                self.render("quiz.html", **template_values)
            else:
                self.write_plain('No such game')
        else:
            self.redirect('/')