README.md
MarkDown
# Email ID Extractor

A Scrapy project to extract email addresses from websites.

## Features

* Extracts email addresses from websites using Scrapy
* Validates email addresses using regular expressions
* Removes duplicate email addresses
* Saves extracted email addresses to a CSV file

## Requirements

* Python 3.8+
* Scrapy 2.4+
* csv 1.0+

## Installation

1. Clone the repository: `git clone https://github.com/your-username/email-id-extractor.git`
2. Navigate to the project directory: `cd email-id-extractor`
3. Install the requirements: `pip install -r requirements.txt`

## Usage

1. Run the spider: `scrapy crawl email_spider`
2. Specify the website to crawl: `scrapy crawl email_spider -a start_url=https://www.example.com`

## Output

The extracted email addresses will be saved to a CSV file named `emails.csv` in the project directory.
