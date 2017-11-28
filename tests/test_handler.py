import pytest

from handler import get_sentiment_csv


def test_get_sentiment_csv():
    params = {
        'queryStringParameters': {
            'q': 'Seahawks'
        },
    }
    print(get_sentiment_csv(params, None))
