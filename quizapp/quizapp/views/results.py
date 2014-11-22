#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class ResultsHandler(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Results')
