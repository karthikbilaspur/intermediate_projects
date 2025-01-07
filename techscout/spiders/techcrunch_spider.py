import scrapy
from bs4 import BeautifulSoup
from techscout.items import TechscoutItem
import logging

class TechcrunchSpider(scrapy.Spider):
    name = 'techcrunch'
    start_urls = ['https://techcrunch.com/']
    crawl_depth = 2

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'depth': 0})

    def parse(self, response):
        try:
            soup = BeautifulSoup(response.body, 'html.parser')
            articles = soup.find_all('article')

            for article in articles:
                item = TechscoutItem()
                item['title'] = article.find('h2').text.strip()
                item['link'] = article.find('a')['href']
                item['description'] = article.find('p').text.strip()

                yield item

            if response.meta['depth'] < self.crawl_depth:
                next_page = soup.find('a', class_='next')
                if next_page:
                    yield response.follow(next_page['href'], self.parse, meta={'depth': response.meta['depth'] + 1})
        except Exception as e:
            logging.error(f"Crawl error: {e}")