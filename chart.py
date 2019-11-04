import json
from datetime import datetime
from dateutil.parser import parse
from pprint import pprint
from textblob import TextBlob

tweets = []
data = []

with open('data-twarc/2015.02.json') as f1:
    for line in f1:
        tweets.append(json.loads(line))

for tweet in tweets:
    sentiment = TextBlob(tweet['text']).sentiment.polarity
    data.append((parse(tweet['created_at']), tweet['text'], sentiment))

pprint(data)