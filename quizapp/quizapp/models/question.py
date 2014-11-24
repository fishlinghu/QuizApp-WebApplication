from google.appengine.ext import ndb

class Question(ndb.model):
	question = ndb.StringProperty()
	correct_ans = ndb.StringProperty()
	wrong_ans = ndb.StringListProperty()
	description = ndb.StringProperty()
	wiki_link = ndb.StringProperty()
	topic = ndb.StringProperty()
