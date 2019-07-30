def analyzeSentiment(text)
    api_key = "4da7e0a5920ffb13aadf6e83ee7ae01ed5e6ae27"#Key to let you access to API
    api_url = "https://language.googleapis.com/v1/documents:analyzeSentiment"#Url To get access to Api
    totalUrl = api_url + "?" + api_key#The total url
    sent = urlib.urlencode({#The information being sent to the API
    #somehow get information from noah to put inside here
    #and pass the information to the sentiment API
    })
    getSentiment = urlfetch.fetch(totalUrl,
        method = urfetch.POST,
        sent = sent
    )
    if getSentiment.status_code == 200:
        returnedAPI = json.loads(getSentiment.content)
    elif getSentiment.status_code == 400:
        message = "Invalid Value/Input, please try again"
        return message
    else:
        message = "Something went wrong going into API" + str(result.status_code) + " " + str(result.content)
        ErrorNotification.new(msg)
        return None, message
    template_vars = {
        'totalSentiment' = returnedAPI['documentSentiment']['score']#extract information from the API return
        'totalMagnitude' = returnedAPI['documentSentiment']['magnitude']
    }
