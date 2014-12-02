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
        	# get the most recent game player by user
        	# here is a problem, we actually need to implement a_ID == user OR b_ID == user
        	# but this db doesn't support OR
        	# my solution is a little ugly
        	q = Game.all()
        	q.filter('a_ID = ', user).order('-create_time')
        	game = q.fetch(1)

        	q = Game.all()
        	q.filter('b_ID = ', user).order('-create_time')
        	game_temp = q.fetch(1)
        	
        	if game.create_time > game_temp.create_time:
        		# user's ID == a_ID
        		your_score = game.a_score
        		opp_score = game.b_score
        	else:
        		# user's ID == b_ID
        		your_score = game.b_score
        		opp_score = game.a_score

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
        	
        	# get the user
        	q = Player.all()
        	q.filter('player_ID = ', user)
        	player = q.fetch(1)

        	# Need a function of score/win/lose to calculate the experience an user get
        	exp = exp_calculator(score, w_o_l)
        	player.experience = player.experience + exp;
        	if player.experience >= player.exp_require[player.level]:
        		# level up
        		player.experience = player.experience - player.exp_require[player.level]
        		player.level = player.level + 1

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
