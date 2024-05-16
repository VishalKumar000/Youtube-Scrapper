"""
scrape video titles and links from YouTube channels listed in a text file named 'subscription.txt'. The collected data is then stored in a JSON file named 'output.json'.
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
