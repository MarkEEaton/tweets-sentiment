import csv
import json
import pandas as pd
import seaborn as sns
from datetime import datetime
from dateutil.parser import parse
from matplotlib import pyplot as plt
from pathlib import Path
from textblob import TextBlob
from pprint import pprint

data = []
error_count = 0

# loop through the twarc archive
pathlist1 = Path("data-twarc/").glob("*.json")
for path in pathlist1:
    with open(str(path)) as f1:
        for line in f1:
            try:
                json_line = json.loads(line)
                sentiment = TextBlob(json_line["text"]).sentiment.polarity
                data.append((json_line["created_at"], json_line["text"], sentiment))
            except json.decoder.JSONDecodeError:
                error_count += 1
                print("Error reading json!")
                pass

# loop through the tcat archive
pathlist2 = Path("data-tcat/").glob("*.csv")
for path in pathlist2:
    with open(str(path), encoding="utf-8") as f2:
        lines = csv.reader(f2)
        next(lines, None)
        for line in lines:
            try:
                sentiment = TextBlob(line[4]).sentiment.polarity
                formatted_date = datetime.strptime(line[2], "%Y-%m-%d %H:%M:%S")
                data.append((formatted_date, line[4], sentiment))
            except:
                error_count += 1
                print("Error reading csv!")
                raise  # raise because passing here would omit too many values

        # two missing months; add None values
        data.append((datetime(2018, 1, 1), "", None))
        data.append((datetime(2018, 2, 1), "", None))

# create a dataframe
df = pd.DataFrame(data=data)
df.columns = ["date", "tweet", "sentiment"]
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

# group by month and plot a chart
df["month"] = df["date"].dt.strftime("%b %Y")
grouped = df.groupby("month", sort=False)["sentiment"].mean().to_frame().reset_index()
grouped.columns = ["month", "mean"]
plt.plot(grouped["month"], grouped["mean"])

# plot total tweets on a scale of 0 to 0.5
grouped_count = df.groupby("month", sort=False).count()
grouped_count["total"] = grouped_count["date"] / 1002 * 0.5
plt.bar(grouped["month"], grouped_count["total"], color="#cccccc")

plt.ylim(-1, 1)
plt.xticks(rotation=90)
plt.margins(x=0)
plt.xlabel("Month")
plt.ylabel("Sentiment\n1 is positive; -1 is negative")
plt.suptitle("Sentiment in tweets about Kingsborough")
plt.legend(("Sentiment", "Number of tweets"), loc="lower right")

# make every fourth tick label visible
ax = plt.gca()
for idx, label in enumerate(ax.xaxis.get_ticklabels()):
    if idx % 4 == 0:
        label.set_visible(True)
    else:
        label.set_visible(False)

sns.set(style="darkgrid")
plt.show()

print("Tweets: ", len(data))
print("Errors: ", error_count)
