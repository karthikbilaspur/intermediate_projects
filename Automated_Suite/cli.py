import argparse
import logging
from web_scraper import scrape_website
from email_sender import send_email
from social_media_bot import post_tweet
from news_aggregator import get_news

logging.config.fileConfig('logging.conf')

def main():
    parser = argparse.ArgumentParser(description='Project CLI')
    parser.add_argument('--scrape', help='URL to scrape')
    parser.add_argument('--email', help='Email recipient')
    parser.add_argument('--tweet', help='Tweet message')
    args = parser.parse_args()

    if args.scrape:
        scrape_website(args.scrape)
    elif args.email:
        send_email("Test", "This is a test email", "your-email@gmail.com", args.email, "your-email-password")
    elif args.tweet:
        post_tweet("your-api-key", "your-api-secret", "your-access-token", "your-access-token-secret", args.tweet)

if __name__ == "__main__":
    main()