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
			# Should add the game ID(key().id()) to the end of player's "game_history" list when a quiz start
			# So this should be done in quiz.py

			# get the user
			player = Player.get_by_id(user)
			game = Game.get_by_id(int(quiz_key))     
			
			gameAnswers = game.question_answers
			playerAAnswers = game.a_ans_list
			playerBAnswers = game.b_ans_list
			playerAScore = 0
			playerBScore = 0
			
			for i in range(5):
				answerPosition = i-1
				correctAnswer = gameAnswers[answerPosition]
				aAnswer = playerAAnswers[answerPosition]
				bAnswer = playerBAnswers[answerPosition]
				
				if aAnswer == correctAnswer:
					playerAScore = playerAScore + 100
					game.a_score_list.append(100)
				else:
					game.a_score_list.append(0)
				
				if bAnswer == correctAnswer:
					playerBScore = playerBScore + 100
					game.b_score_list.append(100)
				else:
					game.b_score_list.append(0)
				
				game.put()
			
			if game.a_ID == player.key().id():
				# user's ID == a_ID
				your_score = playerAScore
				opp_score = playerBScore
			else:
				# user's ID == b_ID
				your_score = playerBScore
				opp_score = playerAScore

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

			# Update the player entity
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
			
			# Need to get the question number from html somehow
			#q = Question.all()
			#q.filter('question_ID = ', question_ID)
			#question = q.fetch(1)

			template_values = {
				'player_a_name': player_a.name, 
				'player_b_name': player_b.name,
				'player_a_score_breakdown': player_a_score_breakdown,
				'player_b_score_breakdown': player_b_score_breakdown,
				'win_or_lose': win_or_lose,
				'level' : player.level,
				'experience': player.experience
				#'description': question.description,
				#'solution': question.solution,
				#'wiki_link': question.wiki_link,
				#'correct_ans': question.correct_ans 
				}
			self.render("result.html", **template_values)

		else:
			self.redirect('/index')
