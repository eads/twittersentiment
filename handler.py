import json
import os
import twitter

from sentiment import search


def get_sentiment(event, context):
    """
    Get sentiment for a search term.
    """
    return search({
        'q': 'trump', 'count': 100
    })
