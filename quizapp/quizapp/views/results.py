#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from google.appengine.ext import db
from quizapp.models.player import Player
from quizapp.models.question import Question
from quizapp.models.game import Game

def exp_calculator(score, w_o_l):
	exp = score * 1 + w_o_l * 20
	return exp

class ResultsHandler(Handler):
	def render_result(self, **kw):
		self.render("result.html", **kw)

	def get(self):
		# self.render_result()
		user = self.session.get('QUIZAPP_USER')
		quiz_key = self.session.get('QUIZAPP_QUIZ')
		
		if user: 
			# get the user
			player = Player.get_by_id(user)
			game = Game.get_by_id(int(quiz_key))     
			
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
				win_or_lose = "You Win!"
				w_o_l = 2
			elif your_score < opp_score:
				# Show you lose
				win_or_lose = "You Lose!"
				w_o_l = 0
			else:
				# Even
				win_or_lose = "The game is a tie!"
				w_o_l = 1

			# Need a function of score/win/lose to calculate the experience an user get
			exp = exp_calculator(your_score, w_o_l)
			if player.experience:
				player.experience = player.experience + exp
			else:
				player.experience = exp

			# Can set how much experiences you need to level-up here
			if player.experience >= 5000:
				# level up
				playerEXP = player.experience - 5000
				player.experience = playerEXP
				playerLevel = player.level + 1
				player.level = playerLevel

			# Update the player entity and add game history
			player.game_history.append(quiz_key)
			player.put()

			player_a = Player.get_by_id(game.a_ID)
			player_b = Player.get_by_id(game.b_ID)

			player_a_score_breakdown = []
			player_b_score_breakdown = []
			# Scoring breakdown for both players
			for score in game.a_score_list:
				player_a_score_breakdown.append(score)

			for score in game.b_score_list:
				player_b_score_breakdown.append(score)
			
			template_values = {
				'player_a_name': player_a.name, 
				'player_b_name': player_b.name,
				'player_a_score_breakdown': player_a_score_breakdown,
				'player_b_score_breakdown': player_b_score_breakdown,
				'win_or_lose': win_or_lose,
				'level' : player.level,
				'experience': player.experience
				}
			self.render("result.html", **template_values)

		else:
			self.redirect('/index')
