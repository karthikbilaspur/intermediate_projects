BOT_NAME = 'techscout'

SPIDER_MODULES = ['techscout.spiders']
NEWSPIDER_MODULE = 'techscout.spiders'

USER_AGENT = 'TechScout (+https://www.example.com)'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'techscout.pipelines.TechscoutPipeline': 300,
}

FEED_FORMAT = 'json'
FEED_URI = 'techcrunch_articles.json'

LOG_FILE = 'logs/crawl_logs.log'
LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 1  # Rate limiting