import pytest

from search import search


@pytest.mark.parametrize('count', [50, 100])
def test_result_count(count):
    """
    Test result count with two different parameters.
    """
    results = search({
        'q': 'china',
        'count': count,
    })
    assert count == len(results)


def test_has_sentiment():
    """
    Test if sentiment key is being applied.
    """
    results = search({
        'q': 'united states of america',
        'count': 1,
    })
    sentiment_keys = sorted(results[0]['sentiment'].keys())
    expected_keys = ['compound', 'neg', 'neu', 'pos']
    assert expected_keys == sentiment_keys
