# -*- coding: utf-8 -*-

from views import Handler
from quizapp.models.player import Player
from users import checkPlayer

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
    def render_homepage(self, **kw):
        self.render("setting.html", **kw)

    def post(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            # Get the value in the form
            account = self.request.get('account')
            name = self.request.get('name')
            intro = self.request.get('intro')
            old_password = self.request.get('old_password')
            new_password = self.request.get('new_password')
            new_password_check = self.request.get('new_password_check')
            
            # Get the player
            player = Player.get_by_id(user)

            # If the user type something in the blank for account
            # He can change his account
            # I am not sure what will happen if he didn't enter anything
            # Will Python just skip the following if statement?
            if account:
                if checkPlayer(account):
                    self.write_plain("Username is already in use. Please use a different username")
                else:
                    player.account = account

            if name:
                if checkPlayerName(name):
                    self.write_plain("This name is already in use. Please use a different name")
                else:
                    player.name = name

            if intro:
                player.intro = intro

            if old_password:
                if old_password == player.password:
                    if new_password==new_password_check:
                        player.password = new_password
                    else:
                        self.write_plain('Verify your new password! Please type again')
                else:
                    self.write_plain('Wrong password!')
            player.put()
            self.redirect('/setting')

        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.render_homepage()