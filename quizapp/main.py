#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from quizapp import urls

application = webapp2.WSGIApplication(
    urls.routes, 
    debug=True
)
