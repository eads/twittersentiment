#!/usr/bin/env python

import json
import os
import sys
import time
import twitter

from afinn import Afinn
from datetime import datetime
from pprint import pprint
from statistics import mean, median
from urllib.parse import urlencode
from vaderSentiment import vaderSentiment as vader

MAX_API_SEARCH = 100

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

    - `params`: A dict of query parameters.
    - `client`: A Twitter API client (optional).

    Returns a dict with results and a summary of the sentiments found.
    """
    tweets = []
    tweets_to_retrieve = int(params.get('count', 20))
    prev_batch = None
    while tweets_to_retrieve > 0:
        search_params = params.copy()
        search_params['q'] = params.get('q', '')
        search_params['count'] = min(tweets_to_retrieve, 100)
        if prev_batch is not None:
            search_params['max_id'] = max(tweet._json['id'] for tweet in prev_batch)
        cur_batch = client.GetSearch(raw_query=urlencode(search_params))
        tweets += [apply_sentiment(result._json) for result in cur_batch]
        tweets_to_retrieve -= MAX_API_SEARCH
        prev_batch = cur_batch

    return tweets

def search_flat(params={}, client=default_client):
    results = search(params, client)
    out = []
    for result in results:
        processed = flatten_dict(result)
        out.append(processed)

    return out

def apply_sentiment(tweet):
    """
    Apply sentiment to a single Tweet.
    """
    tweet['afinn_sentiment'] = afinn_analyzer.score(tweet['text'])
    tweet['vader_sentiment'] = vader_analyzer.polarity_scores(tweet['text'])
    return tweet


def process_summary(results):
    """
    @TODO restore processing
    """
    return '@TODO TK TK'


def flatten_dict(d):
    """
    Flatten a dictionary into one level with keys like 'key.nestedkey'
    """
    def items():
        for key, value in d.items():
            if key.startswith('retweeted') or key.startswith('quoted') or key.startswith('entities'):
                continue
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + "." + subkey, subvalue
            else:
                yield key, value

    return dict(items())


def parse_timestamp(ts):
    """
    Convert Twitter's 'created_at' timestamp into a datetime object
    """
    return datetime.fromtimestamp(time.mktime(time.strptime(ts,'%a %b %d %H:%M:%S +0000 %Y')))

def avg_sentiment(tweet):
  """
  Return the average of the afinn and vader sentiment scores for a tweet
  """
  return (tweet['afinn_sentiment'] + tweet['vader_sentiment']['compound']) / 2.0

def create_histogram(results, output_file):
    """
    Creates a histogram of the results and saves it in output_file.
    """
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


def summarize(results):
    """
    Return a dictionary containing various aggregate statistics about the results.
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
    avg_afinn = None
    median_afinn = None

    if len(afinn_scores):
        avg_afinn = mean(afinn_scores)
        median_afinn = median(afinn_scores)

    vader_scores = [tweet['vader_sentiment']['compound'] for tweet in results]

    avg_vader = None
    median_vader = None
    if len(vader_scores):
        avg_vader = mean(vader_scores)
        median_vader = median(vader_scores)

    return {
        'afinn': {
            'mean': avg_afinn,
            'median': median_afinn,
        },
        'vader': {
            'mean': avg_vader,
            'median': median_vader,
        }
    }


if __name__ == '__main__':
    results = search_flat({
        'q': sys.argv[1:],
        'count': 100,
    })
    pprint(results)
    # print(json.dumps(results, indent=4))
    # pprint(summarize(results))
