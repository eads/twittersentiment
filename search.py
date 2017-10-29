#!/usr/bin/env python

import os
import json
import sys
import twitter

from urllib import urlencode
from vaderSentiment import vaderSentiment as vader

DEFAULT_CLIENT = twitter.Api(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
              consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
              access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN'),
              access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

ANALYZER = vader.SentimentIntensityAnalyzer()


def search(query, client=DEFAULT_CLIENT, analyzer=ANALYZER):
    """
    Search the Twitter API and apply sentiment analysis to the text of each tweet.

    Arguments:

    - `query`: A dict of query parameters.
    - `client`: A Twitter API client (optional).

    Returns a dict with results and a summary of the sentiments found.
    """
    raw_results = client.GetSearch(raw_query=urlencode(query))
    results = [apply_sentiment(result._json, analyzer) for result in raw_results]
    summary = process_summary(results)
    return {
        'results': results,
        'sentiment_summary': summary,
    }


def apply_sentiment(tweet, analyzer):
    vs = analyzer.polarity_scores(tweet['text'])
    tweet['sentiment'] = vs
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
