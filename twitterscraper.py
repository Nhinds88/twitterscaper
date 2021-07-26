import pandas as pd
import numpy as np
import csv
import snscrape.modules.twitter as sntwitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime as dt
import time

# generating datetime objects
from datetime import datetime, timedelta
now = datetime.now()
now = now.strftime('%Y-%m-%d')
yesterday = datetime.now() - timedelta(days = 1)
yesterday = yesterday.strftime('%Y-%m-%d')

#user input
keyword = input('Enter a topic or keyword: ')

#Twitter Scraping
maxTweets = 8000

#Open/create a file to append data to
csvFile = open(keyword + '-sentiment-' + now + '.csv', 'a', newline='', encoding="utf8")

#Use csv writer
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['id','date','tweet',])

for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' lang:en since:' + yesterday + ' until:' + now + ' -filter:links -filter:replies').get_items()):
    if i > maxTweets :
        break
    csvWriter.writerow([tweet.id, tweet.date, tweet.content])
csvFile.close()

# Vader sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Reading CSV file back into our program
df = pd.read_csv('/Users/nicho/Desktop/twitterscraper/'+ keyword +'-sentiment-' + now + '.csv', parse_dates=True, index_col=0)

# Creating sentiment scores columns
df['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df['tweet']]
df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df['tweet']]
df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df['tweet']]
df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df['tweet']]

# Taking averages of sentiment score columns
avg_compound = np.average(df['compound'])
avg_neg = np.average(df['neg']) * -1  # Change neg value to negative number for clarity
avg_neu = np.average(df['neu'])
avg_pos = np.average(df['pos'])

# Counting number of tweets
count = len(df.index)

# Print Statements
print("Since yesterday there has been", count ,  "tweets on " + keyword, end='\n*')
print("Positive Sentiment:", '%.2f' % avg_pos, end='\n*')
print("Neutral Sentiment:", '%.2f' % avg_neu, end='\n*')
print("Negative Sentiment:", '%.2f' % avg_neg, end='\n*')
print("Compound Sentiment:", '%.2f' % avg_compound, end='\n')