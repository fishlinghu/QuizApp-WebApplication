#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import json
import logging
from google.appengine.ext import db
from quizapp.models.question import Question

class AddQuestionsHandler(Handler):
    def render_add_questions(self, **kw):
        self.render("add_questions.html", **kw)

    def get(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            self.render_add_questions()
        else:
            self.redirect('/')
    
    def post(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            try:
                questions = json.loads(self.request.get('questions'))
                count = 0
                list_of_questions = []
                for q in questions['questions']:
                    question = Question(
                        question = q['question'],
                        description = q['description'],
                        correct_ans = q['correct_ans'],
                        wrong_ans = q['wrong_ans'],
                        wiki_link = q['wiki_link'],
                        img_link = q['img_link'],
                        topic_ID = int(q['topic_ID'])
                    )
                    question.put()
                    list_of_questions.append(q)
                    count += 1
                self.render_add_questions(questions=list_of_questions)
            except ValueError:
                self.render_add_questions(error="Invalid JSON inserted.")
        else:
            self.redirect('/')
