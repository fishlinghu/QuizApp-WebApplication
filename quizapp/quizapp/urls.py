#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quizapp.views.homepage import HomepageHandler
from quizapp.views.quiz import QuizHandler 
from quizapp.views.results import ResultsHandler 
from quizapp.views.test import TestHandler
from quizapp.views.questions import QuestionHandler

routes = [
    ('/', HomepageHandler),
    ('/quiz', QuizHandler),
    ('/results', ResultsHandler),
    ('/test', TestHandler),
    ('/questions/(\w+)/', QuestionHandler),
]
