#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class HomepageHandler(Handler):
    def render_homepage(self, **kw):
        self.render("index.html", **kw)

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.render_homepage()
