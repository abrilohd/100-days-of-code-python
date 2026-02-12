from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("TINDER_EMAIL")
PASSWORD = os.getenv("TINDER_PASSWORD")

# chrome_driver_path = "web_scraping_Selenium\chromedriver.exe"
# driver = webdriver.Chrome(executable_path=chrome_driver_path)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
# (window switch will be done after opening the FB login popup)
driver.get("https://tinder.com/app/recs")
sleep(2)

login_button = driver.find_element(By.LINK_TEXT, "Log in")
login_button.click()
sleep(2)

facebook_login = driver.find_element(By.XPATH, '//div[@class="Mend(a)"]') 
facebook_login.click()
driver.window_handles
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)

Email_or_phone_input = driver.find_element(By.XPATH, '//input[@id="email"]') 
Email_or_phone_input.send_keys(EMAIL)

password_input = driver.find_element(By.XPATH, '//input[@id="pass"]')
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.ENTER)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located(By.XPATH, '//*[@id="root"]/div/div[1]/button')
)

start_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/button')
start_button.click()

# CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
print('Waiting captcha to solve...')
solve_res = driver.execute('executeCdpCommand', {
    'cmd': 'Captcha.waitForSolve',
    'params': {'detectTimeout': 10000},
        })
print('Captcha solve status:', solve_res['value']['status'])
print('Navigated! Scraping page content...')

base_window = driver.window_handles[0]
driver.switch_to.window(base_window)
print(driver.title)

sleep(5)
allow_location_button = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
allow_location_button.click()
notifications_button = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
notifications_button.click()
cookies = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[1]/button')
cookies.click()


#Tinder free tier only allows 100 "Likes" per day. If you have a premium account, feel free to change to a while loop.
for n in range(100):

    #Add a 1 second delay between likes.
    sleep(1)

    try:
        print("called")
        like_button = driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_button.click()

    #Catches the cases where there is a "Matched" pop-up in front of the "Like" button:
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element_by_css_selector(".itsAMatch a")
            match_popup.click()

        #Catches the cases where the "Like" button has not yet loaded, so wait 2 seconds before retrying.
        except NoSuchElementException:
            sleep(2)

driver.quit()