import tweepy
import logging

logging.config.fileConfig('logging.conf')

def post_tweet(api_key, api_secret, access_token, access_token_secret, tweet):
    try:
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(tweet)
        logging.info("Tweet posted")
    except Exception as e:
        logging.error(f"Error posting tweet: {e}")


# Usage
api_key = "your-api-key"
api_secret = "your-api-secret"
access_token = "your-access-token"
access_token_secret = "your-access-token-secret"
tweet = "This is a test tweet"
post_tweet(api_key, api_secret, access_token, access_token_secret, tweet)