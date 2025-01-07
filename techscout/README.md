TechScout Web Crawler
Overview
TechScout is a web crawling project designed to extract technology news articles from TechCrunch. The project utilizes Python, Scrapy and BeautifulSoup libraries for efficient web scraping.
Features
Data Extraction: Extracts article titles, links and descriptions.
Data Storage: Stores extracted data in SQLite database.
API Integration: Provides RESTful API for data retrieval.
Crawling Efficiency: Implements asynchronous crawling and rate limiting.
Data Validation: Validates extracted data using predefined schemas.
Requirements
Python 3.8+
Scrapy 2.6+
BeautifulSoup 4.10+
Flask 2.0+
Flask-RestX 0.5+
Project Structure
MarkDown
techscout/
|--- techscout/
|    |--- __init__.py
|    |--- items.py
|    |--- pipelines.py
|    |--- settings.py
|    |--- spiders/
|    |    |--- __init__.py
|    |    |--- techcrunch_spider.py
|--- requirements.txt
|--- scrape.py
|--- techcrunch.db
|--- logs/
|    |--- crawl_logs.log
|--- utils/
|    |--- helpers.py
|    |--- validators.py
|--- api/
|    |--- app.py
|    |--- routes.py
Running the Project
Install requirements: pip install -r requirements.txt
Run the spider: python scrape.py
Run the API: python api/app.py
API Documentation
Access API documentation at http://localhost:5000/swagger.json
Contributing
Contributions are welcome. Fork the repository, make changes and submit a pull request.
License
MIT License
Author

