#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import json
import logging
from google.appengine.ext import db
from quizapp.models.question import Question
from quizapp.models.topic import Topic 

class AddQuestionsHandler(Handler):
    topics = Topic.all()

    def render_add_questions(self, **kw):
        if (self.check_clearance()):
            self.render("add_questions.html", **kw)

    def get(self):
        self.render_add_questions(topics=self.topics)
    
    def post(self):
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
                    topic_ID = int(self.request.get('topic'))
                )
                question.put()
                list_of_questions.append(q)
                count += 1
            self.render_add_questions(topics=self.topics, message="Questions added successfully.", message_type="alert-success", questions=list_of_questions)
        except ValueError:
            self.render_add_questions(topics=self.topics, message="Invalid JSON inserted.", message_type="alert-danger")
