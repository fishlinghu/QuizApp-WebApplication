import webapp2
from quizapp import urls

application = webapp2.WSGIApplication(
    urls.routes, 
    debug=True
)
