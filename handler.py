import json
import os
import twitter

from search import search


def get_sentiment(event, context):
    """
    Get sentiment for a search term.
    """
    return search('trump')
