#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import json
import logging
from google.appengine.ext import db
from quizapp.models.question import Question
from quizapp.models.topic import Topic 

class AddQuestionHandler(Handler):
    topics = Topic.all()

    def render_add_question(self, **kw):
        self.render("add_question.html", **kw)

    def get(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            self.render_add_question(topics=self.topics)
        else:
            self.redirect('/')
    
    def post(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            wrong_ans_list = []
            wrong_ans_list.append(self.request.get('wrong_ans1'))
            wrong_ans_list.append(self.request.get('wrong_ans2'))
            wrong_ans_list.append(self.request.get('wrong_ans3'))
            newquestion = Question(
                question = self.request.get('question'),
                description= self.request.get('description'),
                correct_ans = self.request.get('correct_ans'),
                wrong_ans = wrong_ans_list,
                wiki_link = self.request.get('wiki_link'),
                img_link = self.request.get('img_link'),
                topic_ID = int(self.request.get('topic'))
            )
            newquestion.put()
            self.render_add_question(message="Successfully added new question.", message_type="alert-success", topics=self.topics)
        else:
            self.redirect('/')
