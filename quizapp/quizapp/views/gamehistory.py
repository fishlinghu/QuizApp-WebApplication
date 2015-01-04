#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from setting import checkPlayerName
from quizapp.models.player import Player
from quizapp.models.game import Game

class GameHistoryHandler(Handler):
    def render_gamehistory(self, **kw):
        self.render("gamehistory.html", **kw)

    def get(self):
        user = self.session.get('QUIZAPP_USER')
        if user: 
            # get the user
            player = Player.get_by_id(user)
            player_a_name_list = []
            player_b_name_list = []
            player_a_score_list = []
            player_b_score_list = []
            who_win_list = []
            game_time_list = []
            topic_list = []

            for game_ID in player.game_history:
                game = Game.get_by_id(game_ID)
                player_a = Player.get_by_id(game.a_ID)
                player_b = Player.get_by_id(game.b_ID)
                
                # Get player's name
                player_a_name_list.append(player_a.name)
                player_b_name_list.append(player_b.name)

                # Get both player's scores
                player_a_score_list.append(game.a_score)
                player_b_score_list.append(game.b_score)

                # Get winning message
                if game.who_win == 0:
                    win_message = player_a.name + ' wins!'
                    who_win_list.append(win_message)
                elif game.who_win == 1:
                    win_message = player_b.name + ' wins!'
                    who_win_list.append(win_message)
                else: 
                    who_win_list.append('Even')

                # Get game created time
                game_time_list.append(game.create_time)

                # Get topics
                topic_list.append(game.topic)

            template_values = {
                'player_a_name_list': player_a_name_list,
                'player_b_name_list' : player_b_name_list,
                'player_a_score_list': player_a_score_list,
                'player_b_score_list': player_b_score_list,
                'who_win_list': who_win_list,
                'game_time_list': game_time_list,
                'topic_list': topic_list 
                }
            self.render("gamehistory.html", name = player.account, **template_values)

        else:
            self.redirect('/index')
    def post(self):
        # You can also find a player's game history by keying in his name
        player_name = self.request.get('player_name')
        player = checkPlayerName(player_name)
        if player:
            player_a_name_list = []
            player_b_name_list = []
            player_a_score_list = []
            player_b_score_list = []
            who_win_list = []
            game_time_list = []
            topic_list = []

            for game_ID in player.game_history:
                game = Game.get_by_id(game_ID)
                player_a = Player.get_by_id(a_ID)
                player_b = Player.get_by_id(b_ID)
                
                # Get player's name
                player_a_name_list.append(player_a.name)
                player_b_name_list.append(player_b.name)

                # Get both player's scores
                player_a_score_list.append(game.a_score)
                player_b_score_list.append(game.b_score)

                # Get winning message
                if game.who_win == 0:
                    win_message = player_a.name + ' wins!'
                    who_win_list.append(win_message)
                elif game.who_win == 1:
                    win_message = player_b.name + ' wins!'
                    who_win_list.append(win_message)
                else: 
                    who_win_list.append('Even')

                # Get game created time
                game_time_list.append(game.create_time)

                # Get topics
                topic_list.append(game.topic)
            
            template_values = {
                'player_a_name_list': player_a_name_list,
                'player_b_name_list' : player_b_name_list,
                'player_a_score_list': player_a_score_list,
                'player_b_score_list': player_b_score_list,
                'who_win_list': who_win_list,
                'game_time_list': game_time_list,
                'topic_list': topic_list 
                }
            self.render("gamehistory.html", **template_values)
        else:
            self.write_plain("Sorry, no such player")
            self.render_gamehistory()
