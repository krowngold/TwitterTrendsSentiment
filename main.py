import webapp2
import logging
import jinja2
import os
import json
import tweepy

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        print "\n\n\nIN MAIN PAGE\n\n\n"

        consumer_key = "wYYrMHPuMAye92UVQgmcrCmDc"
        consumer_secret = "oTcsEv0aMF67sOyiMAfjXn7sdzDV3K3t4k0CJTIeS6cfKjLmJV"
        access_token = "NNlVJFrlyItn1bg7rN2TSHgd2pWfinqAvUsGUpY"
        access_token_secret = "9n4P1lz4mZ6Vx6WTrl6BRf8pIgg5fIFO0kGS8Z3U3To4v"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

        api = tweepy.API(auth)
        for tweet in tweepy.Cursor(api.search, q='tweepy').items(10):
            print(tweet.text)

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

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/aboutus', AboutUs)
], debug=True)
