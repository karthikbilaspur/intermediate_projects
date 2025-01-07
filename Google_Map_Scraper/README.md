A Python script that uses Selenium to scrape data from Google Maps.
Features
Scrapes business names and addresses from Google Maps
Uses Selenium for browser automation
Supports headless mode for faster scraping
Requirements
Python 3.8+
Selenium 4.0+
ChromeDriver (for Selenium)
Google Maps API (not required, but recommended for accurate results)
Installation
Clone the repository: git clone https://github.com/your-username/google-maps-scraper.git
Install the requirements: pip install -r requirements.txt
Download the ChromeDriver executable and add it to your system's PATH
Usage
Run the script: python app.py
Enter your query: Enter your query:
The script will scrape the data and print it to the console
Example Output
[
    {
        "name": "Business Name 1",
        "address": "123 Main St, Anytown USA"
    },
    {
        "name": "Business Name 2",
        "address": "456 Elm St, Othertown USA"
    }
]
Contributing
Contributions are welcome! Please submit a pull request with your changes.
License
This project is licensed under the MIT License.
Acknowledgments
Google Maps API for providing accurate and up-to-date data
Selenium for providing a powerful browser automation tool

