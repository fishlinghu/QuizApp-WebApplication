#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler

def exp_calculator(score, w_o_l):
	exp = score * 0.5 + w_o_l * 20
	return exp

class ResultsHandler(Handler):
    def render_result(self, **kw):
        self.render("result.html", **kw)

    def get(self):
        self.render_result()
        user = self.session.get('QUIZAPP_USER')
        if user: 
        	# Should add the game ID to the end of player's "game_history" list when a quiz start
        	# So this should be done in quiz.py

        	# get the user
        	q = Player.all()
        	q.filter('player_ID = ', user)
        	player = q.fetch(1)

        	q = Game.all()
        	q.filter('game_ID', player.game_history[-1])
        	game = q.fetch(1)
        	
        	if game.a_ID == player.player_ID:
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
        		win_or_lose = "You Win!!"
        		w_o_l = 2
        	else if your_score < opp_score:
        		# Show you lose
        		win_or_lose = "You Lose!!"
        		w_o_l = 0
        	else:
        		# Even
        		win_or_lose = "Even Game"
        		w_o_l = 1

        	# Need a function of score/win/lose to calculate the experience an user get
        	exp = exp_calculator(score, w_o_l)
        	player.experience = player.experience + exp;
        	if player.experience >= player.exp_require[player.level]:
        		# level up
        		player.experience = player.experience - player.exp_require[player.level]
        		player.level = player.level + 1

        	# Update the player entity
        	db.put(player)

        	# Scoring breakdown for both players
        	# I don't know if I can send a list to html
        	for score in game.a_score_list:

        	for score in game.b_score_list:

        	# Need to get the question number from html somehow
        	q = Question.all()
        	q.filter('question_ID = ', question_ID)
        	question = q.fetch(1)

        	template_values = {
        		'win_or_lose': win_or_lose,
        		'level' : player.level,
        		'experience': player.experience,
                'description': question.description,
                'solution': question.solution,
                'wiki_link': question.wiki_link,
                'correct_ans': question.correct_ans 
              	}
        	self.render("quiz.html", **template_values)

        else:
        	self.redirect('/index')
