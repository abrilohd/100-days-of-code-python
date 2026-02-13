from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

PROMISED_DOWN = 150
PROMISED_UP = 10
# CHROME_DRIVER_PATH = "C:\Users\App Factory\Downloads\chromedriver-win64"
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

class InternetSpeedTwitterBot:
    def __init__(self):
        # self.driver = webdriver.Chrome(excutable_path=driver_path)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.speedtest.net/")
        
    def get_internet_speed(self):
        sleep(2)
        self.go_button = self.driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[2]/a/span[4]')
        self.go_button.click()
        sleep(70)
        self.up = self.driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        self.down = self.driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/login")
        self.driver.window_handles
        self.twitter_page = self.driver.window_handles[1]
        self.driver.switch_to.window(self.twitter_page)
        sleep(2)
        email = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input')
        password = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input')
        email.send_keys(TWITTER_EMAIL)
        password.send_keys(TWITTER_PASSWORD)
        sleep(2)
        password.send_keys(Keys.ENTER)
        sleep(5)
        tweet_compose = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div')
        tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        tweet_compose.send_keys(tweet)
        sleep(3)
        tweet_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]')
        tweet_button.click()
        sleep(2)
        self.driver.quit()
    
bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()