import csv
import json
import io
import os
import twitter

from datetime import datetime
from sentiment import search, search_flat, summarize


def get_sentiment(event, context):
    """
    Get sentiment for a search term.
    """
    results = search(event['queryStringParameters'])
    summary = summarize(results)
    return {
        'statusCode': 200,
        'body': json.dumps({
            'results': results,
            'summary': summary,
        }),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        },
    }

def get_simple_sentiment(event, context):
    results = search(event['queryStringParameters'])
    summary = summarize(results)
    output = []

    for tweet in results:
        clean = {
            'id_str': tweet['id_str'],
            'user_screen_name': tweet['user']['screen_name'],
            'user_verified': tweet['user']['verified'],
            'text': tweet['text'],
            'created_at': tweet['created_at'],
            'afinn_sentiment': tweet['afinn_sentiment'],
            'vader_sentiment_compound': tweet['vader_sentiment']['compound'],
            'is_media': tweet['is_media']
        }
        output.append(clean)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'results': output,
            'summary': summary,
        }),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        },
    }



def get_sentiment_csv(event, context):
    """
    Get sentiment for a search term.
    """
    results = search_flat(event['queryStringParameters'])
    writer_file =  io.StringIO()

    fieldnames = list(results[0].keys())
    for result in results:
        s1 = set(fieldnames)
        s2 = set(list(result.keys()))
        in_s2 = s2 - s1
        fieldnames = fieldnames + list(in_s2)

    writer = csv.DictWriter(writer_file, fieldnames=sorted(fieldnames))
    writer.writeheader()
    writer.writerows(results)

    csvfilename = 'twittersentiment-{search}-{now}.csv'.format(
            search=event['queryStringParameters'].get('q', 'NULLSEARCH'),
            now=datetime.now().isoformat()
        )

    return {
        'statusCode': 200,
        'body': writer_file.getvalue(),
        'headers': {
            'content-type': 'text/csv',
            'content-disposition': 'attachment; filename="{0}"'.format(csvfilename),
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        }
    }

