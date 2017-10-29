# Apply sentiment analysis to Tweets

Get any result from the Twitter search API and apply sentiment analysis to the body of each Tweet.

Currently uses VADER sentiment analysis with goal of supporting other sentiment analysis algorithms.

This module can be deployed as a service on Amazon Web Services using the serverless framework.

## Install

```
npm install -g serverless
git clone github.com:eads/twittersentiment
cd twittersentiment
virtualenv venv --python=python2.7
source venv/bin/activate
pip install -r requirements.txt
npm install
```

_`npm` lines can be skipped if not deploying to AWS._

You must obtain and set some Twitter credentials:

```
export TWITTER_CONSUMER_KEY="<YOURCONSUMERKEY>"
export TWITTER_CONSUMER_SECRET="<YOURCONSUMERSECRET>"
export TWITTER_ACCESS_TOKEN="<YOURACCESSTOKEN>"
export TWITTER_ACCESS_TOKEN_SECRET="<YOURACCESSTOKENSECRET>"
```

`jq` is optional, but is required for several output examples and highly recommended. On OS X, install it with:

```
brew install jq
```

## Run

### CLI

```
./search.py panama papers
```

This will get first 100 results for the specified term and return the raw JSON.

#### Filtering results with jq

Let's see what people are saying about Randy "Ironstache" Bryce:

```
./search.py Ironstache | jq '[.results[] | {text: .text, screen_name: .user.screen_name, compound: .sentiment.compound, pos: .sentiment.pos, neg: .sentiment.neg, neu: .sentiment.neu}]'
```

And as a CSV, exported to a file:

```
./search.py Ironstache | jq '[.results[] | {text: .text, screen_name: .user.screen_name, compound: .sentiment.compound, pos: .sentiment.pos, neg: .sentiment.neg, neu: .sentiment.neu}]' | jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' > ironstache_sentiment.csv
```

(I know that's annoyingly long but you can play with it just by changing the search term.)

### Tests

```
python -m pytest
```

### Deploy to lambda

TK
