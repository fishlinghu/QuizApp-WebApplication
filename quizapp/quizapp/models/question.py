from google.appengine.ext import db

class Question(db.model):
	question_ID = db.IntegerProperty()
	description = db.StringProperty()
	correct_ans = db.StringProperty()
	wrong_ans = db.StringListProperty()
	solution = db.StringProperty()
	wiki_link = db.StringProperty()
	topic = db.StringProperty()
	topic_ID = db.IntegerProperty()
