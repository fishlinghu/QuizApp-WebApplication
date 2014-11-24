#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class ResultsHandler(Handler):
    def render_result(self, **kw):
        self.render("result.html", **kw)

    def get(self):
        self.render_result()
