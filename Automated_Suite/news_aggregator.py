import feedparser
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

logging.config.fileConfig('logging.conf')

class NewsAggregator:
    def __init__(self, feeds):
        self.feeds = feeds

    def parse_feed(self, feed_url):
        try:
            feed = feedparser.parse(feed_url)
            logging.info(f"Successfully parsed {feed_url}")
            return feed.entries
        except Exception as e:
            logging.error(f"Error parsing {feed_url}: {e}")
            return []

    def extract_articles(self, entries):
        articles = []
        for entry in entries:
            article = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary
            }
            articles.append(article)
        return articles

    def filter_articles(self, articles, keywords):
        filtered_articles = []
        for article in articles:
            for keyword in keywords:
                if keyword.lower() in article['title'].lower():
                    filtered_articles.append(article)
                    break
        return filtered_articles

    def get_news(self, keywords=None):
        news = []
        for feed_url in self.feeds:
            entries = self.parse_feed(feed_url)
            articles = self.extract_articles(entries)
            if keywords:
                articles = self.filter_articles(articles, keywords)
            news.extend(articles)
        return news

    def scrape_article(self, article_url):
        try:
            response = requests.get(article_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            logging.info(f"Successfully scraped {article_url}")
            return soup.find('body').text
        except Exception as e:
            logging.error(f"Error scraping {article_url}: {e}")
            return None


def get_news(feeds, keywords=None):
    aggregator = NewsAggregator(feeds)
    return aggregator.get_news(keywords)


# Usage
feeds = [
    "https://news.google.com/rss/search?q=technology",
    "https://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"
]

keywords = ["AI", "Machine Learning"]
news = get_news(feeds, keywords)

for article in news:
    print(article['title'])
    print(article['link'])
    print(article['published'])
    print(article['summary'])