import unittest
from news_aggregator import get_news
from unittest.mock import patch
from feedparser import FeedParserDict

class TestNewsAggregator(unittest.TestCase):

    @patch('feedparser.parse')
    def test_get_news_success(self, mock_parse):
        mock_feed = FeedParserDict(entries=[{'title': 'Test News'}])
        mock_parse.return_value = mock_feed
        feeds = ["https://news.google.com/rss/search?q=technology"]
        news = get_news(feeds)
        self.assertIsNotNone(news)
    @patch('feedparser.parse')
    def test_get_news_failure(self, mock_parse):
        mock_parse.side_effect = Exception
        feeds = ["https://news.google.com/rss/search?q=technology"]
        news = get_news(feeds)
        self.assertIsNone(news)

    def test_get_news_invalid_feed(self):
        feeds = ["invalid_feed"]
        news = get_news(feeds)
        self.assertIsNone(news)
if __name__ == "__main__":
    unittest.main()