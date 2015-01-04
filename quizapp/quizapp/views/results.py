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
			else:
				# user's ID == b_ID
				your_score = game.b_score
				opp_score = game.a_score
				opponentName = Player.get_by_id(game.a_ID).name

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
			player_a_score_breakdown = game.a_score_list
			player_b_score_breakdown = game.b_score_list
			
			experienceToNextLevel = 5000 - player.experience
			
			template_values = {
							'opponentName' : opponentName,
							'player_a_name': player_a.name, 
							'player_b_name': player_b.name,
							'player_a_score_breakdown': player_a_score_breakdown,
							'player_b_score_breakdown': player_b_score_breakdown,
							'win_or_lose': win_or_lose,
							'level' : player.level,
							'experience': experienceToNextLevel
							}
			
			self.session['QUIZAPP_FINISHED'] = None
			self.render("result.html", **template_values)
		else:
			self.redirect('/index')
