import json
import os
import twitter

from sentiment import search, process_summary


def get_sentiment(event, context):
    """
    Get sentiment for a search term.
    """
    results = search(event['queryStringParameters'])
    summary = process_summary(results)
    return {
        'statusCode': 200,
        'body': json.dumps({
            'results': results,
            'summary': summary,
        }),
    }
