"""
This script utilizes Selenium to scrape video titles and links from YouTube channels listed in a text file named 'subscription.txt'. It automates the process of visiting each channel, scrolling to load all available videos, and extracting their titles and links.

Workflow:
1. It sets up a Selenium WebDriver using Firefox, configured to run in private mode.
2. Reads the list of URLs from 'subscription.txt' and visits each URL.
3. Scrolls down the page to load all available videos.
4. Extracts titles and links of videos using CSS selectors.
5. Stores the titles and links in a list of dictionaries.
6. Writes the collected data into a JSON file named 'output.json'.

Ensure 'subscription.txt' contains the URLs of YouTube channels in the expected format, and adjust the scrolling mechanism if needed to ensure all videos are loaded before extraction.
"""


import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time
import os

driver_path = "/snap/bin/geckodriver"
service = Service(executable_path=driver_path)
options = webdriver.FirefoxOptions()
options.add_argument("-private")

driver = webdriver.Firefox(service=service, options=options)

data = []

try:
    with open(os.getcwd() + '/subscription.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            url = line.strip()
            driver.get(url)

            last_height = driver.execute_script("return document.body.scrollHeight")

            cnt = 5000
            while cnt:
                driver.execute_script("window.scrollBy(0, 500);")  # Scroll down by 500 pixels
                # time.sleep(0.1)
                cnt -= 1

            time.sleep(5)

            titles = driver.find_elements(By.CSS_SELECTOR, '.style-scope.ytd-rich-grid-slim-media > span#video-title')
            links = driver.find_elements(By.CSS_SELECTOR, 'div#contents a#thumbnail')

            arr = []
            # Store title and link pairs in a list of dictionaries
            for idx, title in enumerate(titles):
                entry = {'title': title.text, 'link': links[idx].get_attribute('href')}
                arr.append(entry)
            data.append(arr)

            print(driver.title, len(titles))

except FileNotFoundError:
    print("The file was not found")
except IOError:
    print("An error occurred while reading the file")
finally:
    driver.quit()

# Dump data into a JSON file
with open('output.json', 'w') as json_file:
    json.dump(data, json_file, indent=2)
