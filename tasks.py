import csv
import json
import sys

from invoke import task
from sentiment import search, summarize, create_histogram


@task
def full_search(ctx, query, limit=100):
    """
    Search for a given term and return full JSON object.
    """
    print(json.dumps(
        _search(query, limit),
        indent=4
    ))


@task
def sentiment_search(ctx, query, limit=100, output='json'):
    """
    Search for a given term and get a condensed view of the results: currently
    just text, screen_name, and sentiment scores.
    """
    results = _search(query, limit)
    # import pdb; pdb.set_trace();
    flattened = [{
        'text': result['text'],
        'screen_name': result['user']['screen_name'],
        'vader_compound': result['vader_sentiment']['compound'],
        'vader_neu': result['vader_sentiment']['neu'],
        'vader_neg': result['vader_sentiment']['neg'],
        'vader_pos': result['vader_sentiment']['pos'],
        'afinn_score': result['afinn_sentiment'],
        'url': 'https://twitter.com/_/status/%s' % result['id'],
        'created_at': result['created_at'],
    } for result in results]

    if output == 'json':
        print(json.dumps(flattened, indent=4))
        print("%d tweets retrieved" % len(flattened))
        print("EXQMPLE TWEET: " + str(results[0]))
        summary = summarize(results)
        print("Average sentiment scores:\n   afinn: %f\n   vader: %f\n   overall: %f" % (summary['afinn'], summary['vader'], summary['average']))
        create_histogram(results, 'graph.png')
    else:
        fieldnames = ['text', 'screen_name', 'vader_compound', 'vader_neu', 'vader_neg', 'vader_pos', 'afinn_score', 'url', 'created_at']
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened)


def _search(query, limit):
    tweets = []
    tweets_to_retrieve = limit  # number of Tweets we still need to retrieve
    prev_batch = None
    while tweets_to_retrieve > 0:
        # Keep getting the next page of tweets until we've retrieved enough
        search_params = {'q': query, 'count': min(tweets_to_retrieve, 100)}
        if prev_batch is not None:
            search_params['max_id'] = max(tweet['id'] for tweet in prev_batch)
        cur_batch = search(search_params)
        tweets += cur_batch
        tweets_to_retrieve -= 100
        prev_batch = cur_batch
    return tweets
