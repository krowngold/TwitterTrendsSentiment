import webapp2
import logging
import jinja2
import os
import json

# How do I use my authorization keys without being prone to security issues?
# One website tells me to store my keys as a json file but idk how to do that
# credentials = {}
# credentials['CONSUMER_KEY'] = ...
# credentials['CONSUMER_SECRET'] = ...
# credentials['ACCESS_TOKEN'] = ...
# credentials['ACCESS_SECRET'] = ...
#
# with open("twitter_credentials.json", "w") as file:
#     json.dump(credentials, file)
#     print "dumped files"

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render())

class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/aboutus.html')
        self.response.write(template.render())
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////






#///////////////////////////////////////////////////////////////////////////////////////////////////////////////
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/aboutus', AboutUs)
], debug=True)
