"""
Unit tests for `sentiment.py`, our wrapper for the Twitter API and utilities
for working with the data.
"""
import pytest

from sentiment import search, process_summary


@pytest.mark.parametrize('count', [50, 100])
def test_search_results_count(count):
    """
    Test result count with two different parameters.
    """
    results = search({
        'q': 'sumac',
        'count': count,
    })
    assert count == len(results)


def test_search_results_have_vader_sentiment_keys():
    """
    Test if sentiment key is being applied.
    """
    results = search({
        'q': 'burdock',
        'count': 1,
    })
    sentiment_keys = sorted(results[0]['vader_sentiment'].keys())
    expected_keys = ['compound', 'neg', 'neu', 'pos']
    assert expected_keys == sentiment_keys


def test_search_results_have_afinn_score():
    results = search({
        'q': 'zatar',
        'count': 1,
    })
    assert isinstance(results[0]['afinn_sentiment'], float)


def test_process_summary():
    assert process_summary(results=None) == '@TODO TK TK'
