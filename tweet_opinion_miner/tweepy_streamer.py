from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream

import tweet_credentials
import numpy as np
import pandas as pd

class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth=TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client=API(self.auth)
        self.twitter_user=twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client


    def get_user_tweets(self,num_tweets):
        tweets=[]
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self,num_friends):
        friend_list=[]
        for friend in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_tl_tweets(self,num_tweets):
        home_tl_tweets=[]
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
            home_tl_tweets.append(tweet)
        return home_tl_tweets                        

class TwitterAuthenticator():
    """
    Authenticate twitter api
    """
    def authenticate_twitter_app(self):
        auth=OAuthHandler(tweet_credentials.CONSUMER_KEY,tweet_credentials.CONSUMER_SECRET)
        auth.set_access_token(tweet_credentials.ACCESS_TOKEN,tweet_credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    """
    Class for processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator=TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #This handles handles twitter authentication and connection to twitter api.
        listener=TwitterListener(fetched_tweets_filename)
        auth=self.twitter_authenticator.authenticate_twitter_app()
        stream=Stream(auth,listener)
        stream.filter(track=hash_tag_list,is_async=True)

class TwitterListener(StreamListener): 
    """
    Prints received tweets to stdout.
    """
    def __init__(self,fetched_tweets_filename):
        self.fetched_tweets_filename=fetched_tweets_filename

    def on_data(self,data):
        try:
            #print(data)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
        except BaseException as e:
            print("Error on data:%s" % str(e))        
        return True

    def on_error(self,status):
        if status==420:
            #Returning false on data method in case rate limit occurs
            return False
        print(status)

class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets
    """
    def tweets_to_data_frame(self, tweets):
        df=pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        return df


if __name__=="__main__":

    hash_tag_list=['eden hazard','kylian mbappe','lionel messi']   
    fetched_tweets_filename="tweets_data.json"

    twitter_streamer=TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename,hash_tag_list)

    twitter_client=TwitterClient()
    tweet_analyzer=TweetAnalyzer()
    api=twitter_client.get_twitter_client_api()

    #tweets=api.user_timeline(screen_name="vintageredss", count=20)
    #print(dir(tweets[0]))
    #df=tweet_analyzer.tweets_to_data_frame(tweets)
    #print(df.head(2))
    #twitter_client=TwitterClient('a_nnphil')
    #print(twitter_client.get_user_tweets(1))
    #print(twitter_client.get_friend_list(5)) 
    #print(twitter_client.get_home_tl_tweets(1))  
