#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

class ResultsHandler(Handler):
    def render_info(self, **kw):
        self.render("info.html", **kw)

    def get(self):
        self.render_result()
        user = self.session.get('QUIZAPP_USER')
        if user: 
            # Should add the game ID to the end of player's "game_history" list when a quiz start
            # So this should be done in quiz.py

            # get the user
            player = Player.get_by_id(user)

            template_values = {
                'account': player.account,
                'name' : player.name,
                'experience': player.experience,
                'level': player.level,
                'intro': player.intro
                }
            self.render("info.html", **template_values)

        else:
            self.redirect('/index')
