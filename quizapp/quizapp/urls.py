#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quizapp.views.homepage import HomepageHandler
from quizapp.views.quiz import QuizHandler 
from quizapp.views.results import ResultsHandler 

routes = [
    ('/', HomepageHandler),
    ('/quiz', QuizHandler),
    ('/results', ResultsHandler),
]
