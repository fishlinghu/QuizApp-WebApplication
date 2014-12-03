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
                    """
                        Each q has:
                            question: string
                            correct_ans: string
                            wrong_ans: list of string
                            topic: string
                            wiki: string

                        Each model q has:
                            question_ID Integer generate by count
                            description String is the questions
                            correct_ans String
                            wrong_ans StringList
                            wiki_link String
                            topic String always "alcohol"
                            topic_ID 1
                    """
                    question = Question(
                        question_ID = count,
                        description = q['question'],
                        correct_ans = q['correct_ans'],
                        wrong_ans = q['wrong_ans'],
                        topic = q['topic'],
                        wiki_link = q['wiki'],
                        topic_ID = 1
                    )
                    question.put()
                    list_of_questions.append(q)
                    count += 1
                self.render_add_questions(questions=list_of_questions)
            except ValueError:
                self.render_add_questions(error="Invalid JSON inserted.")
        else:
            self.redirect('/')
