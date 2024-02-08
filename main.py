import time
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"
headers = {"ACCEPT-LANGUAGE": "en-GB,en-US;q=0.9,en;q=0.8",
           "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/121.0.0.0 Safari/537.36"}

zillow_clone_web_data = requests.get(ZILLOW_CLONE_URL, headers=headers).text
soup = BeautifulSoup(zillow_clone_web_data, "html.parser")

# Get links for all the apartments
links_data = soup.find_all("a", class_="property-card-link")
links = [l.get('href') for l in links_data]

# Get all prices
prices_data = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")
prices = [p.text.replace("/", "+").split("+")[0] for p in prices_data]

# Get all addresses
addresses_data = soup.find_all("address")
addresses = [a.text.strip().replace("|", ",") for a in addresses_data]

# Fill the Google form
GFORM_URL = "https://forms.gle/BYPLxbeN1KLhrkKS9"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options)

# Automate the Google form filling
for apartment in range(len(links)):
    driver.get(GFORM_URL)

    time.sleep(2)
    all_inputs = driver.find_elements(By.CSS_SELECTOR, "input.whsOnd.zHQkBf")
    address_input = all_inputs[0]
    price_input = all_inputs[1]
    link_input = all_inputs[2]

    address_input.send_keys(addresses[apartment])
    time.sleep(1.1)
    price_input.send_keys(prices[apartment])
    time.sleep(1.1)
    link_input.send_keys(links[apartment])
    time.sleep(1.1)

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()
