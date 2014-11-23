#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class TestHandler(Handler):
    def render_test(self, **kw):
        self.render("test.html", **kw)

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.render_test(test="foo bar")
