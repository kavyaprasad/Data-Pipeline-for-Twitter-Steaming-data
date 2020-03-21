# Implementing a data pipeline that outputs a machine-learning ready dataset using twitter streaming API
## Introduction
 We are using the Twitter API to search for tweets containing specific keywords and stream this directly into the database. Once we have done this, the data will be available for further analysis at any time. 

## Steps taken to perform the task
 - Created a Twitter account and API credentials
- Downloade any opensource Database - Decided to download MySQL database because of it's widespread use
- Install the Tweepy and mysql-connector Python Libraries
- After looking at the twitter documentation, I found the most important and useful fields to extract for our dataset from the twitter API: username, created_at, tweet, retweet_count and location of the tweet.
- I created an object for my class 'StdOutListener' and extracted all the tweets from the API with the filter '#justinbieber' in it.
- Before storing it in my database, I implemented a few checks
1) Kept a track of Number of tweets: tweetCount
2) Filtering out duplicate tweet by initialising a list and checking if the tweet has already been consumed.
3) Since the previous step has been executed, Number of tweets and Number of unique tweets will remain same.
4) I'm also filtering out on the keyword '#music' or 'music'.
- Final step is to store the tweet and it's related information in the database.

## Future Work
- Build a python process which runs on GCP's Compute Engine which listens to data coming from Twitter and publish to  cloud Pub/Sub topic which can eventually be stored in different destinations.
- Use GCP's  Dataflow to build a job that keeps pulling tweets from Pub/Sub every few seconds.
- Use GCP's in house data warehouse Big Query to store the data.
- Dataflow or Apche Beam can be used to support data parallelism and to support horizontal scaling.
