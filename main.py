import webapp2
import logging
import jinja2
import os
import json
import twitter
import sys
import pprint
reload(sys)
sys.setdefaultencoding('utf8')

consumer_key = "PTHIXCLxsNtC7vOncS6vzHiBu"
consumer_secret = "dl7jsDCHwcB7XHoAY7FZcLSY8ktbCzmnxXZckNgNi0CtoWWvNz"
access_token = "3080354129-r8HhnjK4eYZUG9BopJMgq0cPf7BEmRtrCmEuuIf"
access_token_secret = "bJ6pCD4zQg7wLSV03TehGF6iL8WkDaUscij7lvTT7puHc"

api = twitter.Api(consumer_key = consumer_key,
    consumer_secret=consumer_secret,
    access_token_key= access_token,
    access_token_secret= access_token_secret,
    tweet_mode="extended")
# import urllib
#
# from google.appengine.api import urlfetch

# pjson = codebeautify.json.read()
# pdata = json.loads(pjson)
# print pdata


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

import urllib
from google.appengine.api import urlfetch

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

def split(word):
    return [char for char in word]

class MainPage(webapp2.RequestHandler):
    def POST(self):
        if (self.response.get("search") in codebeautify.json):
            template_vars = {
                "new_location": self.response.get("search")
            }
            template = jinja_env.get_template("templates/main.html")
            self.response.write(template.render(new_location))
        else:
            template = jinja_env.get_template("templates/main.html")
            self.response.write(template.render())

    def get(self):
        print "\n\n\nIN MAIN PAGE\n\n\n"

        trends = api.GetTrendsWoeid(23424977, exclude = None)
        trends.sort(key = lambda x: x.tweet_volume, reverse = True)

        top_trends = []

        while len(top_trends) < 10:
            max = trends[0]
            temp = 0
            for i in range(len(trends)):
                if (not trends[i].tweet_volume == None) and trends[i].tweet_volume > max.tweet_volume:
                    max = trends[i]
                    temp = i

            trends.pop(temp)
            top_trends.append(max)

        search_names = []

        for trend in top_trends:
            new_string = trend.name
            string_array = split(new_string)
            for i in range(len(string_array)):
                if string_array[i] == " ":
                    string_array[i] = "%20"
                elif string_array[i] == "#":
                    string_array[i] = "%23"
            new_string = ''.join(string_array)
            search_names.append(new_string)

        tweet_samples = []

        pp = pprint.PrettyPrinter(indent=4)
        results = []
        for trend in search_names:
            results.append(api.GetSearch(raw_query="q=" + trend + "&result_type=popular&since=2019-07-29&count=1", return_json = True, lang = "English"))

        for status in results:
            temp = status["statuses"]
            print "\n\n\nNEWTWEET\n\n\n"
            print temp[0]["full_text"]
            tweet_samples.append(temp[0]["full_text"])

        template_vars = {
            "top_trends": top_trends,
            "search_names": search_names,
            "tweet_samples": tweet_samples
        }

        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render(template_vars))
        #//////////////////////////////////////////////////////////////////////////////////////////
        api_key = "4da7e0a5920ffb13aadf6e83ee7ae01ed5e6ae27"#Key to let you access to API
        api_url = "https://language.googleapis.com/v1/documents:analyzeSentiment"#Url To get access to Api
        totalUrl = api_url + "?" + api_key#The total url
        packageSent = urllib.urlencode({#The information being sent to the API
        #somehow get information from noah to put inside here
        #and pass the information to the sentiment API
        #lists inside dictionary
            "Request_body" : "My name is jason li, i am very happy"
        })
        getSentiment = urlfetch.fetch(totalUrl,
            method = urlfetch.POST,
            packageSent = packageSent
        )
        if getSentiment.status_code == 200:
            returnedAPI = json.loads(getSentiment.content)
        elif getSentiment.status_code == 400:
            message = "Invalid Value/Input, please try again"
        else:
            message = "Something went wrong going into API" + str(result.status_code) + " " + str(result.content)
            ErrorNotification.new(msg)
        template_vars = {
            'totalSentiment' : returnedAPI['documentSentiment']['score'],
            'totalMagnitude' : returnedAPI['documentSentiment']['magnitude']
        }
        #/////////////////////////////////////////////////////////////////////////////////////////////
class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/aboutus.html')
        self.response.write(template.render())

class Info(webapp2.RequestHandler):
    def get(self):
        template_vars = {
            "tweets": tweets
        }
        template = jinja_env.get_template('templates/info.html')
        self.response.write(template.render())
# class sentiment_analysis(webapp2.RequestHandler):
    #This allows access to the paid API
    # creds = service_account.Credentials.from_service_account_file('/Users/cssi/Desktop/TheFinalProject/TwitterTrendsSentiment/key.json')
    # client = language.LanguageServiceClient(
    #     credentials = creds,
    # )
    # def get(self)
# api_key = "key"#Type the Api KEY
# base_url = api url get#Get the url for the api
# params = {'q' : 'Harry Potter', 'key' : api_key,}#TYPE IN THE PARAMTERS TO CALL FOR INFORMATION
# urllib.urlencodee(param)
# full_url = base_url + "?" + urllib.urlencode(params)
#
# #fetch url
# books_reponse = urlfetch.fetch(full_url).content
# #get json response and convert to a dictionary
# dictionary = json.loads(books_response)
#
# template_vars = {
#     'books' : books_dictionary['items'],
#     }
# book[x][a] in order to get the stuff from the dictionary.

# class sentiment_analysis(webapp2.RequestHandler):
#     #This allows access to the paid API
#     creds = service_account.Credentials.from_service_account_file('/Users/cssi/Desktop/TheFinalProject/TwitterTrendsSentiment/key.json')
#     client = language.LanguageServiceClient(
#         credentials = creds,
#     )
    #This funciton will return the values given by the API
    # def analyze(#someText from the file names of positivie.txt and negative.txt, should be the only passed parameters
    # ):
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
    ('/aboutus', AboutUs),
    # ('/info', Info)
    # ('/', sentiment_analysis)
], debug=True)
