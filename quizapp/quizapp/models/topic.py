from google.appengine.ext import db

class Topic(db.Model):
    name = db.StringProperty()
	description = db.StringProperty()
