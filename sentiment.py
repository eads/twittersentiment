#!/usr/bin/env python

import os
import json
import sys
import twitter

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


def process_summary(results):
    """
    @TODO: Add descriptive stats based on aggregate results.
    """
    return "@TODO TK TK"


if __name__ == '__main__':
    results = search({
        'q': sys.argv[1:],
        'count': 100,
    })
    print(json.dumps(results, indent=4))
