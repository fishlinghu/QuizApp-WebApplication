from google.appengine.ext import db
import datetime

#the result page's information can base on the information in game model and question model
class Game(db.Model):
	create_time = db.DateTimeProperty(auto_now_add=True)
	#user id of two players
	a_ID = db.IntegerProperty()
	b_ID = db.IntegerProperty()
	#used to save a list of question ID for the questions that should appear in this game 
	question_set = db.ListProperty(int)
	#record the answers of each player every round
	a_ans_list = db.ListProperty(bool)
	b_ans_list = db.ListProperty(bool)
	#total socres of two players
	a_score = db.IntegerProperty()
	b_score = db.IntegerProperty()
	#record the scores each player got in every round
	a_score_list = db.ListProperty(int)
	b_score_list = db.ListProperty(int)
