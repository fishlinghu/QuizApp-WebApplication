# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.player import Player

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

            old = self.request.get('old')
            new = self.request.get('new')
            verify = self.request.get('verify')

            # profile.password = new 

            profile.put()
            kw = {
                'password': profile.password,
            }
            self.render_password(**kw)
        else:
            self.redirect('/')
