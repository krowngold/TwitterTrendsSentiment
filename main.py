import webapp2
import logging
import jinja2
import os
import json
# import tweepy
#///////// - Jason Li
# import argparse
# from google.cloud import language
# from google.cloud.language import enums
# from google.cloud.language import types
# from google.cloud import language
# from google.oauth2 import service_account
#///////// - Jason Li
# import tweepy not sure how this one works
# from twitter import twitter
# from TwitterAPI import TwitterAPI


# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)
#
# trends1=api.trends_place(1)
#
# data = trends1[0]
# trends=data['trends']
# names = [trend['name'] for trend in trends]
# # put all the names together with a ' ' separating them
# trendsName = ' '.join(names)
# print(trendsName)

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
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        print "\n\n\nIN MAIN PAGE\n\n\n"

        consumer_key = "wYYrMHPuMAye92UVQgmcrCmDc"
        consumer_secret = "oTcsEv0aMF67sOyiMAfjXn7sdzDV3K3t4k0CJTIeS6cfKjLmJV"
        access_token = "NNlVJFrlyItn1bg7rN2TSHgd2pWfinqAvUsGUpY"
        access_token_secret = "9n4P1lz4mZ6Vx6WTrl6BRf8pIgg5fIFO0kGS8Z3U3To4v"

        # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # auth.set_access_token(access_token, access_token_secret)
        # auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

        # api = tweepy.API(auth)
        # for tweet in tweepy.Cursor(api.search, q='tweepy').items(10):
        #     print(tweet.text)

        # trends1 = api.trends_place(2459115)
        # data = trends1[0]
        # # grab the trends
        # trends = data['trends']
        # # grab the name from each trend
        # names = [trend['name'] for trend in trends]
        # # put all the names together with a ' ' separating them
        # trendsName = ' '.join(names)
        # print(trendsName)
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
