import csv
import json
import io
import os
import twitter

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
    import ipdb; ipdb.set_trace();
    writer.writerows(results)

    return {
        'statusCode': 200,
        'content-type': 'text/csv',
        'body': writer_file.getvalue(),
        'contentDisposition': 'attachments; filename="twittersentiment.csv"',
        # 'headers': {
            # "Access-Control-Allow-Origin" : "*",
            # "Access-Control-Allow-Credentials" : True
        # },
    }

