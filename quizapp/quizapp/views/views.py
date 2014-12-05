#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import jinja2
import os
from webapp2_extras import sessions

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True
)

class Handler(webapp2.RequestHandler):

    def check_clearance(self, classified=True, *a, **kw):
        user = self.session.get('QUIZAPP_USER')
        if (classified and not user):
            self.redirect('/')
            return False
        return True

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def write_plain(self, text):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(text)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, classified=True, **kw):
        self.response.headers['Content-Type'] = 'text/html'
        self.write(self.render_str(template, **kw))

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.write('Test')
