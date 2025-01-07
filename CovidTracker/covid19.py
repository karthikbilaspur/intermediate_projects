import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
import argparse

class CovidTracker:
    """
    A class to track COVID-19 data from the Milken Institute's website.
    """

    def __init__(self, url, output_file):
        """
        Initializes the CovidTracker class with the given URL and output file.
        
        Args:
            url (str): The URL of the webpage containing COVID-19 data.
            output_file (str): The name of the file to save the data to.
        """
        self.url = url
        self.output_file = output_file
        self.html_data = None
        self.data = []
        self.last_updated = None

    def get_covid_data(self):
        """
        Fetches COVID-19 data from the given URL.
        
        Raises:
            requests.exceptions.RequestException: If an error occurs during the HTTP request.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            self.html_data = response.text
            self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")

    def extract_data(self):
        """
        Extracts COVID-19 data from the fetched HTML content.
        """
        if self.html_data:
            soup = BeautifulSoup(self.html_data, 'html.parser')
            data_elements = soup.find_all("div", class_="is_h5-2 is_developer w-richtext")
            self.data = [str(element) for element in data_elements]

    def print_covid_data(self):
        """
        Prints the extracted COVID-19 data in a readable format.
        """
        if self.data:
            print(f"Last updated: {self.last_updated}")
            for i, item in enumerate(self.data):
                print(f"NO {i+1} {item[46:86]}")
        else:
            print("No data available.")

    def save_covid_data(self):
        """
        Saves the extracted COVID-19 data to a file.
        """
        if self.data:
            with open(self.output_file, "w") as file:
                file.write(f"Last updated: {self.last_updated}\n")
                for i, item in enumerate(self.data):
                    file.write(f"NO {i+1} {item[46:86]}\n")
            logging.info(f"Data saved to {self.output_file}")
        else:
            logging.warning("No data available to save.")

    def visualize_data(self):
        """
        Visualizes the extracted COVID-19 data using Matplotlib and Seaborn.
        """
        if self.data:
            # Create a Pandas DataFrame from the extracted data
            df = pd.DataFrame(self.data, columns=["Data"])

            # Plot a bar chart of the top 10 countries by COVID-19 cases
            top_10_countries = df.nlargest(10, "Data")
            plt.figure(figsize=(10, 6))
            sns.barplot(x=top_10_countries.index, y="Data", data=top_10_countries)
            plt.title("Top 10 Countries by COVID-19 Cases")
            plt.xlabel("Country")
            plt.ylabel("COVID-19 Cases")
            plt.show()

            # Plot a line chart of the COVID-19 cases over time
            plt.figure(figsize=(10, 6))
            sns.lineplot(x=df.index, y="Data", data=df)
            plt.title("COVID-19 Cases Over Time")
            plt.xlabel("Time")
            plt.ylabel("COVID-19 Cases")
            plt.show()
        else:
            logging.warning("No data available to visualize.")


def main():
    parser = argparse.ArgumentParser(description="COVID-19 Data Tracker")
    parser.add_argument("-u", "--url", help="URL of the webpage containing COVID-19 data", default="https://covid-19tracker.milkeninstitute.org/")
    parser.add_argument("-o", "--output", help="Name of the file to save the data to", default="covid_data.txt")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    tracker = CovidTracker(args.url, args.output)
    tracker.get_covid_data()
    tracker.extract_data()
    tracker.print_covid_data()
    tracker.save_covid_data()

if __name__ == "__main__":
    main()