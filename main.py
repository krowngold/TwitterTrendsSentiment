import webapp2
import logging
import jinja2
import os
import json
import twitter
import sys
import pprint
import simplejson
import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
import urllib
from google.appengine.api import urlfetch
reload(sys)
sys.setdefaultencoding('utf8')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))


'''
    Unpacking twitter credentials and retrieving woeid numbers from separate json files
'''
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
with open('codebeautify.json') as f:
    city_ids = simplejson.loads(f.read())
'''
    Global methods
'''
def split(word):
    return [char for char in word]
'''
    All the models for the website. Not sure if we're going to implement them.
'''

class Trend(ndb.Model):
    title = ndb.StringProperty(required = True)
    num_tweets = ndb.IntegerProperty(required = True)
    tweet = ndb.StringProperty(required = True)

class Location(ndb.Model):
    name = ndb.StringProperty(required = True)
    trend_keys = ndb.KeyProperty(kind=Trend, required=False, repeated=True)
    date = ndb.DateProperty(required = True)


'''
    All handlers for the website
'''
class MainPage(webapp2.RequestHandler):
    def getSentiment(self, packageSent):
        api_key = "key=AIzaSyD_CyzFIF6FHeVOC4T8BLDAoasBAvDmEmI"#Key to let you access to API
        api_url = "https://language.googleapis.com/v1/documents:analyzeSentiment"#Url To get access to Api
        totalUrl = api_url + "?" + api_key#The total url to access the API
        errorCheck = 2
        print "\n"
        getSentiment = urlfetch.fetch(totalUrl,
            method = urlfetch.POST,
            payload = json.dumps(packageSent),
            headers={'Content-Type': 'application/json'}
        )
        if getSentiment.status_code == 200:
            returnedAPI = json.loads(getSentiment.content)
            template_vars = {
                'totalSentiment' : returnedAPI['documentSentiment']['score'],
                'totalMagnitude' : returnedAPI['documentSentiment']['magnitude']
            }
            return template_vars
        elif getSentiment.status_code == 400:
            message = "Invalid Value/Input, please try again" + str(getSentiment.status_code) + "  " + str(getSentiment.content)
            print message
            return errorCheck
        else:
            message = "Something went wrong going into API" + str(getSentiment.status_code) + " " + str(getSentiment.content)
            print message
            return errorCheck
    def calculateSentiment(self, dictionary):
        totalSentiment = 0
        rating = ""
        totalMagnitude = 0
        currentBothMultiplied = 0
        amountOfValues = len(dictionary)
        for key in dictionary:
            packageSent ={
                "document" : {"type" : "PLAIN_TEXT",
                              "content" : dictionary[key]
                }
            }
            notCurrentSentiment = self.getSentiment(packageSent)
            currentSentiment = notCurrentSentiment['totalSentiment']
            currentMagnitude = notCurrentSentiment['totalMagnitude']
            if currentSentiment >= -1 and currentSentiment <= 1:
                # print currentSentiment
                # print currentMagnitude
                print currentMagnitude
                print currentSentiment
                currentBothMultiplied += (currentSentiment * currentMagnitude)
                # totalSentiment += currentSentiment
                # totalMagnitude += currentMagnitude
                # print totalSentiment
                # print totalMagnitude
                print currentBothMultiplied
            else:
                print str(errorAmount)
        return currentBothMultiplied

    def topTrending(self, code):
        trends = api.GetTrendsWoeid(code, exclude = None)
        trends.sort(key = lambda x: x.tweet_volume, reverse = True)
        top_trends = []
        while len(top_trends) < 5:
            max = trends[0]
            temp = 0
            for i in range(len(trends)):
                if (not trends[i].tweet_volume == None) and trends[i].tweet_volume > max.tweet_volume:
                    max = trends[i]
                    temp = i
            trends.pop(temp)
            top_trends.append(max)
        return top_trends

    def tweetURL(self, trending):
        search_names = []
        for trend in trending:
            new_string = trend.name
            string_array = split(new_string)
            for i in range(len(string_array)):
                if string_array[i] == " ":
                    string_array[i] = "%20"
                elif string_array[i] == "#":
                    string_array[i] = "%23"
            new_string = ''.join(string_array)
            search_names.append(new_string)
        return search_names

    def getTweets(self, search):
        resultsAnswer = []
        for trend in search:
            test = api.GetSearch(raw_query="q="+trend+"%20lang%3Aen&result_type=popular&since=2019-07-31", return_json = True)
            resultsAnswer.append(test)
        return resultsAnswer

    def retrieveTweets(self, topTrends, search, resultList, location):
        tweet_dictionary = {}
        trend_list = []
        for i in range(len(search)):
            trend = topTrends[i]
            status = resultList[i]
            if (len(status["statuses"]) > 0) and (len(status["statuses"][0]) > 0) and len(status["statuses"][0]["full_text"]) > 0:
                status_to_use =  status["statuses"][0]["full_text"]
            else:
                status_to_use = ""
            tweet_dictionary[trend.name] = status_to_use
            trend_key = Trend(title = topTrends[i].name, num_tweets = topTrends[i].tweet_volume, tweet = status_to_use).put()
            trend_list.append(trend_key)
        location_key = Location(name = location, trend_keys = trend_list, date = datetime.datetime.now()).put()
        return tweet_dictionary

    def loadTrends(self, code=23424977, location = "Seattle"):
        pp = pprint.PrettyPrinter(indent=4)
        places = Location.query().fetch()
        for place in places:
            print datetime.datetime.now() == place.date
            if location == place.name and datetime.datetime.now() == place.date:
                location_trends = place.trend_keys
                trending_topics = []
                tweet_content = []
                for key in location_trends:
                    trending_topics.append(key.get().title)
                searching = self.tweetURL(trending_topics)
                for key in location_trends:
                    tweet_content.append(key.get().tweet)
                twt_dictionary = {}
                for i in range(len(search)):
                    trend = trending_topics[i]
                    twt_dictionary[trend] = tweet_content[i]

                template_vars = {
                    "top_trends": trending_topics,
                    "search_names": searching,
                    "tweet_dictionary": twt_dictionary,
                    "new_location": location
                }
            else:
                top_trends = self.topTrending(code)
                search_names = self.tweetURL(top_trends)
                results = self.getTweets(search_names)

                tweet_dictionary = self.retrieveTweets(top_trends, search_names, results, location) #returns dictionary of tweets

                template_vars = {
                    "top_trends": top_trends,
                    "search_names": search_names,
                    "tweet_dictionary": tweet_dictionary,
                    "new_location": location,
                }
                template_vars["sentimentValueScore"] = self.calculateSentiment(template_vars["tweet_dictionary"])
                # print template_vars["sentimentValueScore"]
                if template_vars["sentimentValueScore"] >= 0.5 and template_vars["sentimentValueScore"] <= 10.0:
                    template_vars["rating"] = "Positive"
                elif template_vars["sentimentValueScore"] < 0.5 and template_vars["sentimentValueScore"] > -0.5:
                    template_vars["rating"] = "Mixed"
                else:
                    template_vars["rating"] = "Negative"
                    print "Moved to else"
                # print template_vars["rating"]
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
        print template_vars["rating"]
        print template_vars["sentimentValueScore"]
        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render(template_vars))

    def post(self):
        user_search = self.request.get("search")
        if (self.city_search(user_search, city_ids)):
            template_vars = self.loadTrends(self.city_code(user_search, city_ids), user_search)
        else:
            template_vars = self.loadTrends(2352824, "The United States")
            template_vars["user_search"] = user_search
        template_vars.update()
        template = jinja_env.get_template("templates/main.html")
        self.response.write(template.render(template_vars))

class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/aboutus.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/aboutus', AboutUs),
])
