import tweepy
import time
import os
import dotenv

banner = """
 _______                _           _ 
|__   __|              | |         | |
   | |_      _____  ___| |_ ___  __| |
   | \ \ /\ / / _ \/ _ \ __/ _ \/ _` |
   | |\ V  V /  __/  __/ ||  __/ (_| |
   |_| \_/\_/ \___|\___|\__\___|\__,_|

"""
print(banner)

dotenv.load_dotenv()

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)


def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.TooManyRequests as e:
        print(e)
        time.sleep(10000)
        limit_handler(cursor)
    except StopIteration:
        pass


search = 'etahamed'
numberOfTweets = 2

# like some tweets
for tweet in limit_handler(tweepy.Cursor(api.search_tweets, search).items(numberOfTweets)):
    try:
        tweet.favorite()
        print('I liked a tweet')
        time.sleep(5)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break

# tweet something
api.update_status('Is this bot working? 👀')
