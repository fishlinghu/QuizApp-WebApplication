#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class QuizHandler(Handler):
    def render_quiz(self, **kw):
        self.render("quiz.html", **kw)

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.render_quiz()
