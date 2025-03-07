from web_scraper import scrape_website
from email_sender import send_email
from social_media_bot import post_tweet
from news_aggregator import get_news
from task_automator import job
import logging
from cli import main
from task_automator import sched
def main():
    url = "http://example.com"
    title = scrape_website(url)
    print(title)
    subject = "Test Email"
    message = "This is a test email"
    from_addr = "your-email@gmail.com"
    to_addr = "recipient-email@gmail.com"
    password = "your-email-password"
    send_email(subject, message, from_addr, to_addr, password)
    api_key = "your-api-key"
    api_secret = "your-api-secret"
    access_token = "your-access-token"
    access_token_secret = "your-access-token-secret"
    tweet = "This is a test tweet"
    post_tweet(api_key, api_secret, access_token, access_token_secret, tweet)
    feed_url = "https://news.google.com/rss/search?q=technology"
    news = get_news(feed_url)
    for article in news:
        print(article['title'])
    job()
logging.config.fileConfig('logging.conf')
def main():
    logging.info("Project started")
    main_cli = main()
    sched.start()
if __name__ == "__main__":
    main()