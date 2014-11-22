#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class QuizHandler(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Quiz page')
