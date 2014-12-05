#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quizapp.views.homepage import HomepageHandler
from quizapp.views.index import IndexHandler
from quizapp.views.quiz import QuizHandler
from quizapp.views.submit import SubmitHandler
from quizapp.views.results import ResultsHandler 
from quizapp.views.test import TestHandler
from quizapp.views.questions import QuestionHandler
from quizapp.views.users import LoginHandler
from quizapp.views.users import LogoutHandler
from quizapp.views.users import RegisterHandler
from quizapp.views.message import MessageHandler
from quizapp.views.friend import FriendHandler
from quizapp.views.setting import SettingHandler
from quizapp.views.add_questions import AddQuestionsHandler
from quizapp.views.add_question import AddQuestionHandler
from quizapp.views.add_topic import AddTopicHandler

routes = [
    ('/', HomepageHandler),
    ('/index', IndexHandler),
    ('/quiz/(\w+)/', QuizHandler),
    ('/results', ResultsHandler),
    ('/test', TestHandler),
    ('/questions/(\w+)/', QuestionHandler),
    ('/quiz/submit', SubmitHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/register', RegisterHandler), 
    # I think we will need the following new pages
    # When in the index.html, and click on the corresponding buttons
    # You can go to corresponding new pages
    ('/message', MessageHandler), # Deal with the messages, you can send and read messages 
    ('/info', InfoHandler),  # Show your personal information, maybe everyone can view other people's profile
    ('/setting', SettingHandler), # Change your informations here, such as account, password, name, etc. 
    ('/friend', FriendHandler), # Show your friends list, you can also add/delete friend here
    #('/gamehistory', GamehistoryHandler), # Show your game history, just like result
    ('/add_questions', AddQuestionsHandler),
    ('/add_question', AddQuestionHandler),
    ('/add_topic', AddTopicHandler),
]
