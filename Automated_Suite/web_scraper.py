import requests
from bs4 import BeautifulSoup
import logging

logging.config.fileConfig('logging.conf')

def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        logging.info(f"Successfully scraped {url}")
        return soup.find('title').text
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return None