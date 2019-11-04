import json
from datetime import datetime
from dateutil.parser import parse
from pathlib import Path
from pprint import pprint
from textblob import TextBlob

tweets = []
data = []
error_count = 0

pathlist = Path("data-twarc/").glob("*.json")
for path in pathlist:
    print(str(path))
    with open(str(path)) as f1:
        for line in f1:
            try:
                tweets.append(json.loads(line))
            except json.decoder.JSONDecodeError:
                error_count += 1
                print('Error reading json!')

for tweet in tweets:
    sentiment = TextBlob(tweet['text']).sentiment.polarity
    data.append((parse(tweet['created_at']), tweet['text'], sentiment))

pprint(data)
print("Tweets: ", len(data))
print("Errors: ", error_count)