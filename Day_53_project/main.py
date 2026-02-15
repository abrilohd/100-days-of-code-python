import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
from dotenv import load_dotenv  

load_dotenv()

ZILLO_CLONE = os.getenv("ZILLO_CLONE")
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

response = requests.get(ZILLO_CLONE)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
prices = []
links = []
addresses = []
price_elements = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")
prices = [element.get_text(strip=True).replace("/mo", "").split("+")[0] for element in price_elements]

link_elements = soup.select(".StyledPropertyCardDataWrapper a")
links = [element["href"] for element in link_elements]
print(f"There are {len(links)} links to individual listings in total: \n")
print(links)

address_elements = soup.find_all("address", text=True)
addresses = [element.get_text(strip=True) for element in address_elements]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

for i in range(len(links)):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfxeGyJy-9W1mpUjRfMlJs3KpQox__O_l5ep8yzI6twwhu0lg/viewform?usp=dialog")
    sleep(2)
    
    first_answer = driver.find_element(By.XPATH, '//input[@aria-labelledby="i1 i4"]')
    first_answer.send_keys(addresses[i])

    second_answer = driver.find_element(By.XPATH, '//input[@aria-labelledby="i6 i9"]')
    second_answer.send_keys(prices[i])

    thired_answer = driver.find_element(By.XPATH, '//input[@aria-labelledby="i11 i14"]')
    thired_answer.send_keys(links[i])

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    sleep(1)
    # another_answer = driver.find_element(By.XPATH, '//div[@class="c2gzEf"]/a')
    # another_answer.click()
