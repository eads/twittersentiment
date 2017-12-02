import csv
import json
import sys

from invoke import task
from sentiment import search_flat, summarize, create_histogram


@task
def sentiment_search(ctx, query, limit=100):
    """
    Search for a given term and get a condensed view of the results: currently
    just text, screen_name, and sentiment scores.
    """
    results = search_flat({'q': query, 'count': limit})
    print(json.dumps(results, indent=4))
    print("%d tweets retrieved" % len(results))
