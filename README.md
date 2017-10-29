# Apply sentiment analysis to Tweets

Get any result from the Twitter search API and apply sentiment analysis to the body of each Tweet.

Currently uses VADER sentiment analysis with goal of supporting other sentiment analysis algorithms.

This module can be deployed as a service on Amazon Web Services using the serverless framework.

## Install

Requirements:

* Python 3 (`brew install python3` on OS X with Homebrew)
* virtualenv (`pip3 install virtualenv`)
* nodejs (`brew install node` on OS X with Homebrew; only required for deployment)
* jq (`brew install jq` on OS X with Homebrew`, required for convenience functions)

```
git clone github.com:eads/twittersentiment
cd twittersentiment
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
npm install -g serverless
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

## Command line interface

### Condensed results

Get latest tweets about the Seahawks in JSON format:

```
invoke sentiment-search "seahawks"
```

Get latest tweets about the Seahawks in CSV format:

```
invoke sentiment-search "seahawks" -o csv
```

Write those tweets to a csv file:

```
invoke sentiment-search "seahawks" -o csv > seahawks-search.csv
```

### Full search

Get full Twitter API results with sentiment scores added:

```
invoke full_search "los angeles"
```

### Basic CLI

_No need to use this. Nonetheless, it exists._

```
./sentiment.py "panama papers"
```

This will get first 100 results for the specified term and return the raw JSON.


### Tests

```
python -m pytest
```

### Deploy to lambda

TK
