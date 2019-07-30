import webapp2
import logging
import jinja2
import os
import json
# import twitter


#///////// - Jason Li
# import argparse
# from google.cloud import language
# from google.cloud.language import enums
# from google.cloud.language import types
# from google.cloud import language
# from google.oauth2 import service_account
#///////// - Jason Li

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        print "\n\n\nIN MAIN PAGE\n\n\n"

        consumer_key = "PTHIXCLxsNtC7vOncS6vzHiBu"
        consumer_secret = "dl7jsDCHwcB7XHoAY7FZcLSY8ktbCzmnxXZckNgNi0CtoWWvNz"
        access_token = "3080354129-r8HhnjK4eYZUG9BopJMgq0cPf7BEmRtrCmEuuIf"
        access_token_secret = "bJ6pCD4zQg7wLSV03TehGF6iL8WkDaUscij7lvTT7puHc"

        # api = twitter.Api(consumer_key = consumer_key,
        #     consumer_secret=consumer_secret,
        #     access_token_key= access_token,
        #     access_token_secret= access_token_secret)
        #
        # trends = api.GetTrendsWoeid(2459115, exclude = None)
        # for i in range(1, 11):
        #     print trends[i]
        #     print "\n"

        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render())

class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/aboutus.html')
        self.response.write(template.render())


# class sentiment_analysis(webapp2.RequestHandler):
#     #This allows access to the paid API
#     creds = service_account.Credentials.from_service_account_file('/Users/cssi/Desktop/TheFinalProject/TwitterTrendsSentiment/key.json')
#     client = language.LanguageServiceClient(
#         credentials = creds,
#     )
    #This funciton will return the values given by the API
    #def analyze(#someText from the file names of positivie.txt and negative.txt, should be the only passed parameters
    #):
        #
    #def print():
        #print out the things that analyze() returns
        #check in the command line for the results
        #print it out via the website later on


#Where do i put access token?
#How do I stop accessing the api
#how do I cache the files?



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/aboutus', AboutUs)
    # ('/', sentiment_analysis)
], debug=True)
