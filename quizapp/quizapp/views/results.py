#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class ResultsHandler(Handler):
    def get(self):
        self.write_plain('Results')
