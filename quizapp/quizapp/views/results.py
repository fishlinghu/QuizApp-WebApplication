#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
from google.appengine.ext import db
from quizapp.models.player import Player
from quizapp.models.question import Question
from quizapp.models.game import Game

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
				opponentName = Player.get_by_id(game.b_ID).name
				opponentLevel = Player.get_by_id(game.b_ID).level
			else:
				# user's ID == b_ID
				your_score = game.b_score
				opp_score = game.a_score
				opponentName = Player.get_by_id(game.a_ID).name
				opponentLevel = Player.get_by_id(game.a_ID).level

			# record who win the game
			if game.a_score > game.b_score:
				game.who_win = 0
			elif game.a_score < game.b_score:
				game.who_win = 1
			else:
				game.who_win = 2
			game.put()

			# Check who wins
			if your_score > opp_score:
				# Show you win
				win_or_lose = "You Win!"
			elif your_score < opp_score:
				# Show you lose
				win_or_lose = "You Lose!"
			else:
				# Even
				win_or_lose = "The game is a tie!"

			player_a = Player.get_by_id(game.a_ID)
			player_b = Player.get_by_id(game.b_ID)

			# Scoring breakdown for both players
			a_breakdown = game.a_score_list
			b_breakdown = game.b_score_list
			player_a_score_breakdown = []
			player_b_score_breakdown = []
			i = 1
			
			for score in a_breakdown:
				infoA = str(i) + ": " + str(score)
				player_a_score_breakdown.append(infoA)
				i = i + 1
			
			i = 1
			
			for score in b_breakdown:
				infoB = str(i) + ": " + str(score)
				player_b_score_breakdown.append(infoB)
				i = i + 1
			
			template_values = {
							'name' : player.account,
							'opponentName' : opponentName,
							'opponentLevel': opponentLevel,
							'player_a_name': player_a.name, 
							'player_b_name': player_b.name,
							'player_a_score_breakdown': player_a_score_breakdown,
							'player_b_score_breakdown': player_b_score_breakdown,
							'win_or_lose': win_or_lose,
							'level' : player.level,
							'experience': player.experience
							}
			
			self.session['QUIZAPP_FINISHED'] = None
			self.render("result.html", **template_values)
		else:
			self.redirect('/index')
