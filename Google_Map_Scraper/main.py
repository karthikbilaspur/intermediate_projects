from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv

app = Flask(__name__)

# Set up the webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(options=options)

# Function to scrape data from Google Maps
def scrape_data(query):
    try:
        driver.get("https://www.google.com/maps")
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        results = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".section-result")))
        data = []
        for result in results:
            name = result.find_element_by_css_selector(".section-result-title").text
            address = result.find_element_by_css_selector(".section-result-location").text
            data.append({"name": name, "address": address})
        return data
    except TimeoutException:
        return []
    except Exception as e:
        return []

# Route to handle form submission
@app.route('/scrape', methods=['GET'])
def scrape():
    query = request.args.get('query')
    data = scrape_data(query)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)