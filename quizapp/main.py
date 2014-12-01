#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from quizapp import urls

config = {}
config["webapp2_extras.sessions"] = {
    "secret_key": "47fhbdh890gtue3i",
}

application = webapp2.WSGIApplication(
    urls.routes, 
    debug=True,
    config=config
)
