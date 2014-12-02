#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quizapp.views.homepage import HomepageHandler
from quizapp.views.index import IndexHandler
from quizapp.views.quiz import QuizHandler 
from quizapp.views.results import ResultsHandler 
from quizapp.views.test import TestHandler
from quizapp.views.questions import QuestionHandler
from quizapp.views.users import LoginHandler
from quizapp.views.users import LogoutHandler
from quizapp.views.users import RegisterHandler

routes = [
    ('/', HomepageHandler),
    ('/index', IndexHandler),
    ('/quiz/(\w+)/', QuizHandler),
    ('/results', ResultsHandler),
    ('/test', TestHandler),
    ('/questions/(\w+)/', QuestionHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/register', RegisterHandler), 
    # I think we will need the following new pages
    # When in the index.html, and click on the corresponding buttons
    # You can go to corresponding new pages
    ('/message', MessageHandler), # Deal with the messages, you can send and read messages 
    ('/info', InfoHandler),  # Show your personal information, maybe everyone can view other people's profile
    ('/setting', SettingHandler), # Change your informations here, such as account, password, name, etc. 
    ('/friend', FriendHandler) # Show your friends list, you can also add/delete friend here
]
