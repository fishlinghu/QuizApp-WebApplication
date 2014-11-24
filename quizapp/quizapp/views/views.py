#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True
)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def write_plain(self, text):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(text)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.response.headers['Content-Type'] = 'text/html'
        self.write(self.render_str(template, **kw))

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.write('Test')
