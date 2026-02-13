from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")


class InstaFollower:
    
    def __init__(self):
        # Keep browser open so you can manually log out
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def login(self):
      # Avoid bot-like behaviour and try not to run your script too often.
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(4.2)
        
        username = self.driver.find_element(by=By.NAME, value="username")
        username.send_keys(USERNAME)
        
        password = self.driver.find_element(by=By.NAME, value="password")
        password.send_keys(PASSWORD)
        
        time.sleep(1)
        password.send_keys(Keys.ENTER)
        
        wait = WebDriverWait(self.driver, 15)
        save_login = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@role='button' and .//text()[contains(.,'Not now')]]")))
        save_login.click()
        
    #     print("Scroll box found")
                 
    def find_followers(self):
        self.driver.get("https://www.instagram.com/developers_team/")
        wait = WebDriverWait(self.driver, 20)
        
        followers_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/followers/')]")))
        followers_btn.click()
        
        time.sleep(8)
        
        scroll_box = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")))
        print("Scroll box found")
        for _ in range(5):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
            time.sleep(2)
            
    def follow(self):
        all_buttons = self.driver.find_elements(By.XPATH, "//button[.//div[text()='Follow']]")
        
        for button in all_buttons:
            try:
                button.click()
                time.sleep(1.1)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel_button.click()
        
def follow(self):
    wait = WebDriverWait(self.driver, 10)

    followed = 0
    MAX_FOLLOWS = 342341  # safe limit

    while followed < MAX_FOLLOWS:
        try:
            follow_button = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[.//div[text()='Follow']]"
                ))
            )

            self.driver.execute_script("arguments[0].click();", follow_button)
            followed += 1
            time.sleep(2)

        except ElementClickInterceptedException:
            try:
                cancel = self.driver.find_element(
                    By.XPATH, "//button[text()='Cancel']"
                )
                cancel.click()
                time.sleep(1)
            except:
                pass

        except:
            print("No more Follow buttons found.")
            break   

bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()