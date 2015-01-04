from google.appengine.ext import db
from datetime import datetime

class Message(db.Model):
	message_ID = db.IntegerProperty()
	topic = db.StringProperty()
	content = db.TextProperty()
	sender_ID = db.IntegerProperty()
	receiver_ID = db.IntegerProperty()
	create_time = db.DateTimeProperty()
