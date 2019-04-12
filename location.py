import tweepy
import json
from pymongo import MongoClient
import twitter_credentials2

MONGO_HOST = 'mongodb://localhost/usa_db'

LOCATION = [-127.3, 24.1, -65.9, 51.8] #USA coordinates

consumer_key = twitter_credentials2.CONSUMER_KEY
consumer_secret = twitter_credentials2.CONSUMER_SECRET
access_token = twitter_credentials2.ACCESS_TOKEN
access_token_secret = twitter_credentials2.ACCESS_TOKEN_SECRET


class StreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        try:
            client = MongoClient(MONGO_HOST)
            db = client.usa_db

            datajson = json.loads(data)

            created_at = datajson['created_at']

            # only get tweets that have geo location enabled
            if datajson['coordinates']:
                print("Tweet collected at " + str(created_at))
                db.usa_tweets_collection.insert_one(datajson)  # insert into db

        except Exception as e:
            print(e)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)

keywords = ['bts', 'korea', '#bts']
streamer.filter(track=keywords, locations=[-180,-90,180,90])