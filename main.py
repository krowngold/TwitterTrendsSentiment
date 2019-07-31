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
class Tweet(ndb.Model):
    text = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)

class Trend(ndb.Model):
    title = ndb.StringProperty(required = True)
    num_tweets = ndb.IntegerProperty(required = True)
    date = ndb.StringProperty(required = True)

class Location(ndb.Model):
    name = ndb.StringProperty(required = True)


'''
    All handlers for the website
'''

class MainPage(webapp2.RequestHandler):

    def loadTrends(self, code=23424977, location = "Seattle"):
        pp = pprint.PrettyPrinter(indent=4)
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
        results = []
        for trend in search_names:
            results.append(api.GetSearch(raw_query="q=" + trend + "&result_type=popular&since=2019-07-31&count=5", return_json = True, lang = "English"))

        tweet_dict = {}
        for trend in top_trends:
            for status in results:
                if trend.name in status["statuses"][0]["full_text"]:
                    temp = status["statuses"]
                    if not temp:
                        print "exiting status[statuses]"
                    elif not temp[0]:
                        print "exiting dictionary"
                    elif not temp[0]["full_text"]:
                        print "no text in this status"
                    else:
                        tweet_dict[trend.name] = temp[0]["full_text"]

        pp.pprint(tweet_dict)



        # pp.pprint(tweet_dict)
            # print ("\n\nNEW STATUS")
            # pp.pprint(temp)
        #     tweet_samples.append(temp[0]["full_text"])
        #     tweet_samples.append(temp[0]["full_text"])

        template_vars = {
            "top_trends": top_trends,
            "search_names": search_names,
            "tweet_dict": tweet_dict,
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

    def getSentiment(self,packageSent):
        api_key = "key=AIzaSyD_CyzFIF6FHeVOC4T8BLDAoasBAvDmEmI"#Key to let you access to API
        api_url = "https://language.googleapis.com/v1/documents:analyzeSentiment"#Url To get access to Api
        totalUrl = api_url + "?" + api_key#The total url to access the API
        errorCheck = 2
        print packageSent
        print "\n"
        print json.dumps(packageSent)
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
            return template_vars['totalSentiment']
        elif getSentiment.status_code == 400:
            message = "Invalid Value/Input, please try again" + str(getSentiment.status_code) + "  " + str(getSentiment.content)
            print message
            return errorCheck
        else:
            message = "Something went wrong going into API" + str(getSentiment.status_code) + " " + str(getSentiment.content)
            print message
            return errorCheck

    def get(self):
        print "\n\n\nIN MAIN PAGE\n\n\n"
        template_vars = self.loadTrends()
        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render(template_vars))

        # totalSentiment = 0
        # rating = ""
        # errorAmount = 0
        # listOfTweets = template_vars["tweet_samples"]
        # amountOfValues = len(listOfTweets)
        # for element in listOfTweets:
        #     packageSent ={
        #         "document" : {"type" : "PLAIN_TEXT",
        #                       "content" : element
        #         }
        #     }
        #     currentSentiment = self.getSentiment(packageSent)
        #     if currentSentiment >= -1 and currentSentiment <= 1:
        #         totalSentiment += currentSentiment
        #     else:
        #         errorAmount += 1
        # amountOfValues -= errorAmount
        # averageSentiment = totalSentiment/amountOfValues
        # if averageSentiment > 0.25 <= 1.0:
        #     print "Positive average"
        #     print averageSentiment
        #     renderRatings = {
        #         "rating" : "Positive - Average"
        #     }
        #     self.response.write(template.render(renderRatings))
        # elif averageSentiment < 0.25 and averageSentiment > -0.25:
        #     print "Neutral average"
        #     print averageSentiment
        #     renderRatings = {
        #         "rating" : "Neutral - Average"
        #     }
        #     self.response.write(template.render(renderRatings))
        # elif averageSentiment < -0.25:
        #     print "Negative average"
        #     print averageSentiment
        #     renderRatings = {
        #         "rating" : "Negative - Average"
        #     }
        #     self.response.write(template.render(renderRatings))
        # else:
        #     print averageSentiment
        #     print "Something went wrong, Call either Jason, Noah or Ethan for fix(Not Free)"

    def post(self):
        user_search = self.request.get("search")
        if (self.city_search(user_search, city_ids)):
            template_vars = self.loadTrends(self.city_code(user_search, city_ids), user_search)
        else:
            template_vars = self.loadTrends(2352824, "The United States")
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
], debug=True)
