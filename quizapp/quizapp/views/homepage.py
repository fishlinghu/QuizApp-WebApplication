#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class HomepageHandler(Handler):
    def render_homepage(self, **kw):
        self.render("homepage.html", **kw)

    def get(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            self.redirect('/index')
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.render_homepage()
