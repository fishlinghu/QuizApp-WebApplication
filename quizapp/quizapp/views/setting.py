# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.player import Player
# from users import checkPlayer

def checkPlayerName(name):
    #Query Datastore for player
    q = db.Query(Player)
    q.filter('name =', name)
    results = q.fetch(1)
        
    #Check if no such player exists
    if results:
        return results
    else :
        return False

class SettingHandler(Handler):
    def render_setting(self, **kw):
        self.render("setting.html", **kw)

    def get(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            profile = Player.get_by_id(user)
            kw = {
                'name': profile.name,
                'intro': profile.intro,
                'account': profile.account
            }
            self.render_setting(**kw)
        else:
            self.redirect('/')

    def post(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            profile = Player.get_by_id(user)
            name = self.request.get('name')
            intro = self.request.get('intro')
            profile.name = name
            profile.intro = intro
            profile.put()
            kw = {
                'name': profile.name,
                'intro': profile.intro,
                'account': profile.account
            }
            self.render_setting(**kw)
        else:
            self.redirect('/')
