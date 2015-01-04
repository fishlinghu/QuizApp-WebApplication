#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import random
import json
import logging
from google.appengine.ext import db
from quizapp.models.game import Game
from quizapp.models.player import Player

def exp_calculator(score, w_o_l):
    exp = score * 1 + w_o_l * 20
    return exp

class ProcessHandler(Handler):
    def render_process(self, **kw):
        self.render("process.html", **kw)

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = self.session.get('QUIZAPP_USER')
        quiz_key = self.session.get('QUIZAPP_QUIZ')
        waiting = self.session.get('QUIZAPP_FINISHED')
        game = Game.get_by_id(int(quiz_key))
        
        if user:
            player = Player.get_by_id(user)
            if game.a_ID == player.key().id():
                opponentName = Player.get_by_id(game.b_ID).name
            else:
                opponentName = Player.get_by_id(game.a_ID).name

            if not waiting:           
                if game.a_ID == player.key().id():
                    # user's ID == a_ID
                    your_score = game.a_score
                    opp_score = game.b_score
                else:
                    # user's ID == b_ID
                    your_score = game.b_score
                    opp_score = game.a_score

                # Check who wins
                if your_score > opp_score:
                    # Show you win
                    w_o_l = 2
                elif your_score < opp_score:
                    # Show you lose
                    w_o_l = 0
                else:
                    # Even
                    w_o_l = 1

                # Need a function of score/win/lose to calculate the experience an user get
                playerEXP = 0
                exp = exp_calculator(your_score, w_o_l)
                
                if player.experience:
                    playerEXP = player.experience % 5000
                    player.experience = player.experience + exp
                    playerEXP = playerEXP + exp
                else:
                    player.experience = exp
                    playerEXP = exp
                    
                
                # Update the player entity and add game history
                player.game_history.append(quiz_key)
                player.put()
                
                # Can set how much experiences you need to level-up here               
                if playerEXP >= 5000:
                    # level up
                    playerLevel = player.level + 1
                    player.level = playerLevel
                    player.put()
                
                self.session['QUIZAPP_FINISHED'] = True
                self.render_process(name = player.name, opponentName = opponentName)
            else:
                if len(game.a_ans_list) >= 5:
                    if len(game.b_ans_list) >= 5:
                        self.redirect('/results')
                    else:
                        self.render_process(name = player.name, opponentName = opponentName)
                else:
                    self.render_process(name = player.name, opponentName = opponentName)
        else:
            self.redirect('/')