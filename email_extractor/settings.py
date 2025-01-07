BOT_NAME = 'email_extractor'

SPIDER_MODULES = ['email_extractor.spiders']
NEWSPIDER_MODULE = 'email_extractor.spiders'

USER_AGENT = 'email_extractor (+https://www.example.com)'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'email_extractor.pipelines.EmailPipeline': 300,
}

CONCURRENT_REQUESTS = 10
DOWNLOAD_DELAY = 1