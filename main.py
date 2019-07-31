import webapp2
import logging
import jinja2
import os
import json
import twitter
import sys
import pprint
import simplejson
from google.appengine.api import users
from google.appengine.ext import ndb

reload(sys)
sys.setdefaultencoding('utf8')

# consumer_key = "PTHIXCLxsNtC7vOncS6vzHiBu"
# consumer_secret = "dl7jsDCHwcB7XHoAY7FZcLSY8ktbCzmnxXZckNgNi0CtoWWvNz"
# access_token = "3080354129-r8HhnjK4eYZUG9BopJMgq0cPf7BEmRtrCmEuuIf"
# access_token_secret = "bJ6pCD4zQg7wLSV03TehGF6iL8WkDaUscij7lvTT7puHc"

with open("twitter_credentials.json") as f:
    creds = simplejson.loads(f.read())
    for cred in creds:
        consumer_key = cred["consumer_key"]
        consumer_secret = cred["consumer_secret"]
        access_token = cred["access_token"]
        access_token_secret = cred["access_token_secret"]

api = twitter.Api(consumer_key = consumer_key,
    consumer_secret=consumer_secret,
    access_token_key= access_token,
    access_token_secret= access_token_secret,
    tweet_mode="extended")
# import urllib
#
# from google.appengine.api import urlfetch


print "file size: " + str(os.path.getsize('codebeautify.json'))
# city_ids_file = open("codebeautify.json")
with open('codebeautify.json') as f:
    city_ids = simplejson.loads(f.read())

#///////// - Jason Li
# import argparse
# from google.cloud import language
# from google.cloud.language import enums
# from google.cloud.language import types
# from google.cloud import language
# from google.oauth2 import service_account
#///////// - Jason Li

import urllib
from google.appengine.api import urlfetch


jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

def split(word):
    return [char for char in word]

class Tweet(ndb.Model):
    text = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)

class Trend(ndb.Model):
    title = ndb.StringProperty(required = True)
    num_tweets = ndb.IntegerProperty(required = True)
    date = ndb.StringProperty(required = True)

class Location(ndb.Model):
    name = ndb.StringProperty(required = True)

class MainPage(webapp2.RequestHandler):
    def loadTrends(self, code=23424977, location = "Seattle"):
        trends = api.GetTrendsWoeid(code, exclude = None)
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
            pp.pprint(temp)
            # tweet_samples.append(temp[0]["full_text"])
            # tweet_samples.append(temp[0]["full_text"])

        template_vars = {
            "top_trends": top_trends,
            "search_names": search_names,
            "tweet_samples": tweet_samples,
            "new_location": location
        }

        return template_vars

    def city_search(self, input, city_list):
        for city in city_list:
            if city["name"] == input:
                return True
        return False

    def city_code(self, input, city_list):
        for city in city_list:
            if city["name"] == input:
                return city["woeid"]
        return 1


    def get(self):
        print "\n\n\nIN MAIN PAGE\n\n\n"
        template_vars = self.loadTrends()

        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render(template_vars))

    def post(self):
        user_search = self.request.get("search")
        if (self.city_search(user_search, city_ids)):
            template_vars = self.loadTrends(self.city_code(user_search, city_ids), user_search)
        else:
            template_vars = self.loadTrends(2352824, "The United States")
        template_vars.update()
        template = jinja_env.get_template("templates/main.html")
        self.response.write(template.render(template_vars))




        #//////////////////////////////////////////////////////////////////////////////////////////
        # api_key = "4da7e0a5920ffb13aadf6e83ee7ae01ed5e6ae27"#Key to let you access to API
        # api_url = "https://language.googleapis.com/v1/documents:analyzeSentiment"#Url To get access to Api
        # totalUrl = api_url + "?" + api_key#The total url
        # packageSent = urllib.urlencode({#The information being sent to the API
        # #somehow get information from noah to put inside here
        # #and pass the information to the sentiment API
        # #lists inside dictionary
        #     "Request_body" : "My name is jason li, i am very happy"
        # })
        # getSentiment = urlfetch.fetch(totalUrl,
        #     method = urlfetch.POST,
        #     packageSent = packageSent
        # )
        # if getSentiment.status_code == 200:
        #     returnedAPI = json.loads(getSentiment.content)
        # elif getSentiment.status_code == 400:
        #     message = "Invalid Value/Input, please try again"
        # else:
        #     message = "Something went wrong going into API" + str(result.status_code) + " " + str(result.content)
        #     ErrorNotification.new(msg)
        # template_vars = {
        #     'totalSentiment' : returnedAPI['documentSentiment']['score'],
        #     'totalMagnitude' : returnedAPI['documentSentiment']['magnitude']
        # }
#         api_key = "key=AIzaSyD_CyzFIF6FHeVOC4T8BLDAoasBAvDmEmI"#Key to let you access to API
#         api_url = "https://language.googleapis.com/v1/documents:analyzeSentiment"#Url To get access to Api
#         totalUrl = api_url + "?" + api_key#The total url
# #The information being sent to the API
# #somehow get information from noah to put inside here
# #and pass the information to the sentiment API
# #lists inside dictionary
#         packageSent ={
#             "document" : {"type" : "PLAIN_TEXT",
#                           "content" : "My name is jason and im very happy"
#             }
#         }
#         print packageSent
#         print "\n"
#         print json.dumps(packageSent)
#         getSentiment = urlfetch.fetch(totalUrl,
#             method = urlfetch.POST,
#             payload = json.dumps(packageSent),
#             headers={'Content-Type': 'application/json'}
#         )
#
#         if getSentiment.status_code == 200:
#             returnedAPI = json.loads(getSentiment.content)
#             template_vars = {
#                 'totalSentiment' : returnedAPI['documentSentiment']['score'],
#                 'totalMagnitude' : returnedAPI['documentSentiment']['magnitude']
#             }
#             print template_vars
#             print("Checking 123")
#         elif getSentiment.status_code == 400:
#             message = "Invalid Value/Input, please try again" + str(getSentiment.status_code) + "  " + str(getSentiment.content)
#             print message
#         else:
#             message = "Something went wrong going into API" + str(getSentiment.status_code) + " " + str(getSentiment.content)
#             print message
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
