#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2

class Handler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Test')
