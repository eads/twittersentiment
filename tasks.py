import csv
import json
import sys

from invoke import task
from sentiment import search


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
    else:
        fieldnames = ['text', 'screen_name', 'vader_compound', 'vader_neu', 'vader_neg', 'vader_pos', 'afinn_score', 'url', 'created_at']
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened)


def _search(query, limit):
    return search({'q': query, 'count': limit})
