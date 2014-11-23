#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class QuizHandler(Handler):
    def get(self):
        self.write_plain('Quiz page')
