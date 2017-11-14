#!/usr/bin/env python

import os
import json
import sys
import twitter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import time

from afinn import Afinn
from urllib.parse import urlencode
from vaderSentiment import vaderSentiment as vader

default_client = twitter.Api(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
              consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
              access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN'),
              access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

afinn_analyzer = Afinn()
vader_analyzer = vader.SentimentIntensityAnalyzer()


def search(params={}, client=default_client):
    """
    Search the Twitter API and apply sentiment analysis to the text of each tweet.

    Arguments:

    - `query`: A dict of query parameters.
    - `client`: A Twitter API client (optional).

    Returns a dict with results and a summary of the sentiments found.
    """
    results = client.GetSearch(raw_query=urlencode(params))
    return [apply_sentiment(result._json) for result in results]


def apply_sentiment(tweet):
    """
    Apply sentiment to a single Tweet.
    """
    tweet['afinn_sentiment'] = afinn_analyzer.score(tweet['text'])
    tweet['vader_sentiment'] = vader_analyzer.polarity_scores(tweet['text'])
    return tweet

# Convert Twitter's 'created_at' timestamp into a datetime object
def parse_timestamp(ts):
    return datetime.fromtimestamp(time.mktime(time.strptime(ts,'%a %b %d %H:%M:%S +0000 %Y')))

# Return the average of the afinn and vader sentiment scores for a tweet
def avg_sentiment(tweet):
  return (tweet['afinn_sentiment'] + tweet['vader_sentiment']['compound']) / 2.0

# Creates a histogram of the results and saves it in output_file.
def create_histogram(results, output_file):
    fig, ax = plt.subplots(1,1)
    dates = [parse_timestamp(tweet['created_at']) for tweet in results]
    sentiment_vals = [avg_sentiment(tweet) for tweet in results]

    months = mdates.MonthLocator()  # every month
    days = mdates.DayLocator()  # every day of the month

    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))

    datemin = min(dates)
    datemax = max(dates)
    ax.set_xlim(datemin, datemax)

    ax.plot(dates, sentiment_vals)
    ax.xaxis_date()
    plt.xlabel('Date')
    plt.ylabel('Average sentiment score')
    plt.show()
    plt.savefig(output_file)

def process_summary(results):
    """
    Print descriptive stats based on aggregate results.
    @TODO use pyplot to display some charts. Ideas for charts:
    - average scores over time
    - average scores grouped by location
    - histogram of frequency distribution for each sentiment score

    @TODO add more stats:
    - median
    - stdev
    - modality summary
    - most frequent terms used in these tweets
    - most common timezones from which people tweeted?
    """

    afinn_scores = [tweet['afinn_sentiment'] for tweet in results]
    vader_scores = [tweet['vader_sentiment']['compound'] for tweet in results]
    avg_afinn = (sum(afinn_scores) + 0.0) / len(afinn_scores)
    avg_vader = (sum(vader_scores) + 0.0) / len(vader_scores)
    avg_overall = (avg_afinn + avg_vader) / 2.0
    return "Average sentiment scores:\n   afinn: %f\n   vader: %f\n   overall: %f" % (avg_afinn, avg_vader, avg_overall)

if __name__ == '__main__':
    results = search({
        'q': sys.argv[1:],
        'count': 100,
    })
    print(json.dumps(results, indent=4))
    print(process_summary(results))
