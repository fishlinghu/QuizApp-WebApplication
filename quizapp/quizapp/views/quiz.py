#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import random
from google.appengine.ext import db
from quizapp.models.game import Game
from quizapp.models.question import Question
from google.appengine.api import channel

class QuizUpdater(Game):
    quiz = None
    
    def __init__(self, quiz):
        self.quiz  = quiz
        
    def get_quiz(self):
        return quiz
    
    def get_quiz_message(self):
        quizUpdate = {
                      'a_ID' : self.quiz.a_ID,
                      'b_ID' : self.quiz.b_ID,
                      'question_set' : self.quiz.question_set,
                      'a_ans_list' : self.quiz.a_ans_list,
                      'b_ans_list' : self.quiz.b_ans_list,
                      'a_score' : self.quiz.a_score,
                      'b_score' : self.quiz.b_score,
                      'a_score_list' : self.quiz.a_score_list,
                      'b_score_list' : self.quiz.b_score_list
                      }
        return json.dumps(quizUpdate)
    
    def send_update(self):
        channel.send_message(self.quiz.a_ID + self.game.key().id(), self.get_game_message())
        if self.quiz.b_ID:
            channel.send_message(self.quiz.b_ID + self.game.key().id(), self.get_game_message())

class QuizHandler(Handler):
    def render_quiz(self, **kw):
        self.render("quiz.html", **kw)

    def get(self, topic):      
        self.response.headers['Content-Type'] = 'text/html'
        user = self.session.get('QUIZAPP_USER')
        quiz_key = self.session.get('QUIZAPP_QUIZ')
        if user:
            if not quiz_key:
                q = db.Query(Game)
                q.filter('b_ID', None)
                q.filter('topic', topic) 
                quiz = q.get()
                
                if not quiz:
                    q = db.Query(Question)
                    q.filter('topic =', topic)
        
                    questions = q.count()
                    questions2 = []
        
                    for i in range(5):
                        questionNumber = random.randint(0, questions - 1)
                        questions2.append(questionNumber)
                        
                    quiz = Game(
                                a_ID = user,
                                question_set = questions2,
                                a_ans_list = [],
                                b_ans_list = [],
                                a_score = 0,
                                b_score = 0,
                                a_score_list = [],
                                b_score_list = []
                                )
                    quiz.put()
                    quiz_key = quiz.key().id()
                else:
                    quiz_key = quiz.key().id()
            
            else:
                quiz = Game.get_by_id(quiz_key)               
            
            if quiz:
                token = channel.create_channel(str(user) + str(quiz_key))
                template_values = {
                    'token': token,
                    'me': user,
                    'quiz_key': quiz_key,
                    'initial_message': QuizUpdater.get_quiz_message()
                }
                self.render("quiz.html", **template_values)
            else:
                self.write_plain('No such game')
        else:
            self.redirect('/')
