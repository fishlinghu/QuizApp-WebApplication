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
    ('/quiz', QuizHandler),
    ('/results', ResultsHandler),
    ('/test', TestHandler),
    ('/questions/(\w+)/', QuestionHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/register', RegisterHandler)
]
