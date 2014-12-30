#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.player import Player
from quizapp.views.users import *
from webapp2_extras import security
from google.appengine.ext import db

class PasswordHandler(Handler):
    def render_password(self, **kw):
        self.render("password.html", **kw)

    def get(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            profile = Player.get_by_id(user)
            kw = {
                'account': profile.account
            }
            self.render_password(**kw)
        else:
            self.redirect('/')

    def post(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            profile = Player.get_by_id(user)

            kw = {
                'account': profile.account
            }

            old = self.request.get('old')
            new = self.request.get('new')
            verify = self.request.get('verify')

            old_hash = security.hash_password(old, method='sha512', pepper=secretPepper)
            if profile.password == old_hash:
                if new == verify:
                    profile.password = security.hash_password(new, method='sha512', pepper=secretPepper)
                    profile.put()
                    self.render_password(message='Password changed.', message_type='alert-success', **kw)
                else:
                    self.render_password(message='New password does not match verification', message_type='alert-danger', **kw)
            else:
                self.render_password(message='Mistake in old password.', message_type='alert-danger', **kw)

            # profile.password = new 

            # profile.put()
            # kw = {
            #     'password': profile.password,
            # }
            # self.render_password(**kw)
        else:
            self.redirect('/')
