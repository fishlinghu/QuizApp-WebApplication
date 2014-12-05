#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import json
import logging
from google.appengine.ext import db
from quizapp.models.topic import Topic

class AddTopicHandler(Handler):
    def render_add_topic(self, **kw):
        if (self.check_clearance()):
            self.render("add_topic.html", **kw)

    def get(self):
        self.render_add_topic()
    
    def post(self):
        name = (self.request.get('name'))
        description = (self.request.get('description'))
        topic = Topic(
            description = description,
            name = name
        )
        topic.put()
        self.render_add_topic(success="New topic " + name + " added.")
