from google.appengine.ext import db

class Question(db.Model):
    question = db.StringProperty()
    description = db.StringProperty()
    correct_ans = db.StringProperty()
    wrong_ans = db.StringListProperty()
    wiki_link = db.StringProperty()
    img_link = db.StringProperty()
    topic_ID = db.IntegerProperty()
