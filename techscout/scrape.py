import scrapy
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess(settings={'FEED_FORMAT': 'json', 'FEED_URI': 'techcrunch_articles.json'})
process.crawl('techcrunch')
process.start()