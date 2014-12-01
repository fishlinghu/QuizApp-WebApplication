#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from google.appengine.ext import db
from quizapp.models.game import Game
from google.appengine.api import channel

class QuizHandler(Handler):
    def render_quiz(self, **kw):
        self.render("quiz.html", **kw)

    def get(self): 
        self.response.headers['Content-Type'] = 'text/html'
        user = self.session.get('QUIZAPP_USER')
        quiz_key = self.session.get('QUIZAPP_QUIZ')
        quiz = None
        if user:
            if not quiz_key:
                quiz = Game(
                    a_ID = user,
                    question_set = [1, 2, 3, 4, 5],
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
                q = db.Query(Game)
                q.filter('id =', quiz_key)
                quiz = q.get()
                if not quiz.b_ID:
                    quiz.b_ID = user
                    quiz.put()

            quiz_link = 'http://localhost:8080/quiz/' + str(quiz_key)

            if quiz:
                token = channel.create_channel(str(user) + str(quiz_key))
                template_values = {
                    'token': token,
                    'me': user,
                    'quiz_key': quiz_key,
                    'quiz_link': quiz_link
                }
                self.render("quiz.html", **template_values)
            else:
                self.write_plain('No such game')
        else:
            self.redirect('/')
