#!/usr/bin/env python

import math
import json
import os
import sys
import time
import twitter

from afinn import Afinn
from collections import Counter
from datetime import datetime, timedelta
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
    days = params.get('days', '')
    search_params = params.copy()
    print(days)
    if days is not None and days != '' and days.isdigit():
        days = int(days)
        tweets = []
        tweets_per_day = math.ceil(search_params['count'] / (days * 1.0))
        today = datetime.now()
        for days_ago in range(1, days+1):
            day = today - timedelta(days_ago)
            search_params['until'] = day.strftime("%Y-%m-%d")
            search_params['count'] = tweets_per_day
            (results, maxid) = search_helper(search_params)
            tweets += results
            search_params['max_id'] = maxid
        return tweets
    return search_helper(params, client)[0]

def search_helper(params={}, client=default_client):
    tweets = []
    tweets_to_retrieve = int(params.get('count', 100))
    prev_batch = None
    max_id = 0
    print(tweets_to_retrieve)
    while tweets_to_retrieve > 0:
        search_params = params.copy()
        search_params['q'] = params.get('q', '')
        search_params['count'] = min(tweets_to_retrieve, 100)
        if max_id > 0:
            search_params['max_id'] = max_id
#cur_batch = [tweet for tweet in client.GetSearch(raw_query=urlencode(search_params)) if tweet._json['id'] != search_params['max_id']]
        print(search_params)
        cur_batch = client.GetSearch(raw_query=urlencode(search_params))
        print(cur_batch)
        tweets += [apply_sentiment(result._json) for result in cur_batch]
        num_tweets_retrieved = len(cur_batch)
        if num_tweets_retrieved > 0:
            max_id = max(tweet._json['id'] for tweet in cur_batch)
        if num_tweets_retrieved < 99:
            break
        tweets_to_retrieve -= num_tweets_retrieved
        prev_batch = cur_batch

    return (tweets, max_id)


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

# Return a JSON array of histogram buckets.
def create_histogram(results):
    """
    Creates a histogram of the results and saves it in output_file.
    """
    fig, ax = plt.subplots(1,1)
    dates = [parse_timestamp(tweet['created_at']) for tweet in results]
    sentiment_vals = [avg_sentiment(tweet) for tweet in results]

def find_freq_keywords(results, n):
    # Return the n most frequent keywords that show up in the tweets
    word_counts = Counter()
    for tweet in results:
        for keyword in tweet['text'].split(' '):
            word_counts[keyword] += 1
    return word_counts.most_common(n)

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

    keywords = find_freq_keywords(results, 5)

    return {
        'afinn': {
            'mean': avg_afinn,
            'median': median_afinn,
        },
        'vader': {
            'mean': avg_vader,
            'median': median_vader,
        },
        'keywords': keywords
    }


if __name__ == '__main__':
    results = search_flat({
        'q': sys.argv[1:],
        'count': 100,
    })
    pprint(results)
    # print(json.dumps(results, indent=4))
    # pprint(summarize(results))
