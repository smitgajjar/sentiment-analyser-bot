from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import re
import twitter_credentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class TwitterClient():
	def __init__(self, twitter_user=None):
		self.auth = TwitterAuthenticator().authenticate_app()
		self.twitter_client = API(self.auth)
		self.twitter_user = twitter_user

	def get_twitter_client_api(self):
		return self.twitter_client

	def get_user_timeline_tweets(self, num_tweets):
		my_tweets = []
		for t in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
			my_tweets.append(t)
		return my_tweets

	def get_friend_list(self, num_friends):
		friend_list=[]
		for f in Cursor(self.twitter_client.friends).item(num_friends):
			friend_list.append(f)
		return friend_list

	def get_home_timeline_tweets(self, num_tweets):
		home_timeline_tweets = []
		for t in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_tweets):
			home_timeline_tweets.append(t)
		return home_timeline_tweets


class TwitterAuthenticator():
	
	def authenticate_app(self):
		auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
		return auth


class TwitterStreamer():

	def __init__(self):
		self.twitter_authenticator=TwitterAuthenticator()

	def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
		listener = TwitterListener(fetched_tweets_filename)
		auth=self.twitter_authenticator.authenticate_app()	
		stream = Stream(auth, listener)
		stream.filter(track=hash_tag_list)	


class TwitterListener(StreamListener):

	def  __init__(self, fetched_tweets_filename):
		self.fetched_tweets_filename = fetched_tweets_filename

	def on_data(self, data):
		try:
			print(data)
			with open(self.fetched_tweets_filename, 'a') as tf:
				tf.write(data)
			return True
		except BaseException as e:
			print('Error on data', str(e))

	def on_error(self, status):
		if status == 420:
			#if rate limit gets exceeded!
			return False
		print(status)


class TweetAnalyser():

	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
	
	def analyse_sentiment(self, tweet):
		analysis = TextBlob(self.clean_tweet(tweet))

		return analysis.sentiment.polarity
		if analysis.sentiment.polarity > 0:
			return 1
		elif analysis.sentiment.polarity == 0:
			return 0
		else:
			return -1

	def tweets_to_data_frame(self, tweets):
		df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
		
		df['id']=np.array([tweet.id for tweet in tweets])
		df['date']=np.array([tweet.created_at for tweet in tweets])
		df['likes']=np.array([tweet.favorite_count for tweet in tweets])
		df['device']=np.array([tweet.source for tweet in tweets])
		df['retweets']=np.array([tweet.retweet_count for tweet in tweets])
		df['length']=np.array([len(tweet.text) for tweet in tweets])

		return df