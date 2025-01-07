import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
import re

class EmailItem(Item):
    email = Field()

class EmailSpider(CrawlSpider):
    name = "email_spider"
    start_urls = [
        'https://www.example.com',  # replace with the website you want to crawl
    ]
    rules = (
        Rule(LinkExtractor(), callback='parse_email', follow=True),
    )

    def parse_email(self, response):
        emails = response.css('a[href^="mailto:"]::attr(href)').get()
        for email in emails:
            email = email.replace('mailto:', '')
            # Validate email using regular expression
            if self.validate_email(email):
                item = ItemLoader(item=EmailItem())
                item.add_value('email', email)
                yield item.load_item()

    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, email):
            return True
        return False