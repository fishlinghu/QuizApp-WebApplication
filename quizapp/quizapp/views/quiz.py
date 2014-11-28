#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.game import Game

class QuizHandler(Handler):
    def render_quiz(self, **kw):
        self.render("quiz.html", **kw)

    def get(self, user_id, quiz_id):
        self.response.headers['Content-Type'] = 'text/html'
        self.write_plain("User_id: " + user_id + "\nQuiz_id: " + quiz_id)
        user = user_id
        quiz_key = quiz_id
        quiz = None
        if user:
            if not quiz_key:
                quiz_key = user_id
                quiz = Game(
                    game_ID = quiz_key,
                    a_ID = user,
                    question_set = [1, 2, 3, 4, 5],
                    a_ans_list = [],
                    b_ans_list = [],
                    a_score = 0,
                    b_score = 0,
                    a_score_list = []
                    b_score_list = []
                )
                quiz.put()
            else:
                guiz = Quiz.get_by_key_name(quiz_key)
                if not quiz.b_ID:
                    quiz.b_ID = user
                    quiz.put()

            quiz_link = 'http://localhost:8080/quiz/' + quiz_key

            if quiz:
                token = channel.create_channel(user_id + quiz_key)
                template_values = {
                    'token': token,
                    'me': user_id(),
                    'quiz_key': quiz_key,
                    'quiz_link': quiz_link,
                    'initial_message': QuizUpdater(quiz).get_quiz_message()
                }
                self.render("quiz.html", **template_values)
