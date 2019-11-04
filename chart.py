import json
import pandas as pd
from datetime import datetime
from dateutil.parser import parse
from matplotlib import pyplot as plt
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
    data.append((tweet['created_at'], tweet['text'], sentiment))

df = pd.DataFrame(data=data)
df.columns = ["date", "tweet", "sentiment"]
df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
df['month'] = df['date'].dt.strftime('%Y-%m')
grouped = df.groupby('month')['sentiment'].mean()
grouped.columns = ["month", "mean"]
grouped.plot(x="month", y="mean")
plt.show()


print(grouped)
print("Tweets: ", len(data))
print("Errors: ", error_count)