import unittest
from social_media_bot import post_tweet
from unittest.mock import patch
from tweepy import TweepError

class TestSocialMediaBot(unittest.TestCase):

    @patch('tweepy.API.update_status')
    def test_post_tweet_success(self, mock_update_status):
        mock_update_status.return_value = True
        api_key = "your-api-key"
        api_secret = "your-api-secret"
        access_token = "your-access-token"
        access_token_secret = "your-access-token-secret"
        tweet = "This is a test tweet"
        post_tweet(api_key, api_secret, access_token, access_token_secret, tweet)
        mock_update_status.assert_called_once()

    @patch('tweepy.API.update_status')
    def test_post_tweet_failure(self, mock_update_status):
        mock_update_status.side_effect = TweepError
        api_key = "your-api-key"
        api_secret = "your-api-secret"
        access_token = "your-access-token"
        access_token_secret = "your-access-token-secret"
        tweet = "This is a test tweet"
        post_tweet(api_key, api_secret, access_token, access_token_secret, tweet)
        mock_update_status.assert_called_once()

    def test_post_tweet_invalid_tweet(self):
        api_key = "your-api-key"
        api_secret = "your-api-secret"
        access_token = "your-access-token"
        access_token_secret = "your-access-token-secret"
        tweet = ""
        post_tweet(api_key, api_secret, access_token, access_token_secret, tweet)

if __name__ == "__main__":
    unittest.main()