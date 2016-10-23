import config
import time
import twitter

from app.models import Tweet
from app.emojis import *
from app import app, db


NB_TWEETS = 100

api = twitter.Api(consumer_key=config.consumer_key,
                consumer_secret=config.consumer_secret,
                access_token_key=config.access_token,
                access_token_secret=config.access_token_secret,
                timeout=60*5)
i = 0

while True:

    time.sleep(0.1) # avoid overpinging API


    stream = api.GetStreamFilter(track=emojis)

    for status in stream:

        try:
            text = status['text']
            try:
                print text
                tweet = Tweet(text)
                db.session.add(tweet)
                db.session.commit()
                i += 1
            except:
                print "Commit failed"
                db.session.rollback()
        except:
            print "Error decoding stream"

    if i > NB_TWEETS:
        break
    elif i % 5 == 0:
        print "-------------------"
        print "| Added %i tweets |" % i
        print "-------------------"
