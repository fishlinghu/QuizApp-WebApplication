#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.player import Player

class InfoHandler(Handler):
    def render_info(self, **kw):
        self.render("info.html", **kw)

    def get(self, account):
        user = self.session.get('QUIZAPP_USER')

        # Get the users profile which is viewed
        q = Player.all()
        q.filter('account =', account)
        profile = q.get()

        if user: 
            # player = Player.get_by_id(user)

            template_values = {
                'account': profile.account,
                'name' : profile.name,
                'experience': profile.experience,
                'level': profile.level,
                'intro': profile.intro
                }
            self.render_info(**template_values)
        else:
            self.redirect('/index')
