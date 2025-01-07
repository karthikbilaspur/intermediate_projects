import unittest
from web_scraper import scrape_website
from unittest.mock import patch
from requests.exceptions import RequestException

class TestWebScraper(unittest.TestCase):

    @patch('requests.get')
    def test_scrape_website_success(self, mock_get):
        mock_response = {'status_code': 200}
        mock_get.return_value = mock_response
        url = "http://example.com"
        title = scrape_website(url)
        self.assertIsNotNone(title)

    @patch('requests.get')
    def test_scrape_website_failure(self, mock_get):
        mock_get.side_effect = RequestException
        url = "http://example.com"
        title = scrape_website(url)
        self.assertIsNone(title)

    def test_scrape_website_invalid_url(self):
        url = "invalid_url"
        title = scrape_website(url)
        self.assertIsNone(title)

if __name__ == "__main__":
    unittest.main()