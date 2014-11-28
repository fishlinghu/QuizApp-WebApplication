from google.appengine.ext import db

class Player(db.model):
	player_ID = db.IntegerProperty()
	account = db.StringProperty()
	password = db.StringProperty()
	name = db.StringProperty()
	intro = db.StringProperty()
	#information about the player's level and experience
	#need a regulation about how can a player level-up
	level = db.IntegerProperty()
	experience = db.IntegerProperty()
	#store a list of friends' ID 
	friend_list = db.ListProperty()
	#store the id of games played before
	game_history = db.ListProperty()
