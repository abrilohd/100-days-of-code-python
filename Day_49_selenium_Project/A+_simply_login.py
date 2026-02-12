from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("http://10.172.76.5/index.php/login")

driver.find_element(By.NAME, "user_name").send_keys("1234567")
driver.find_element(By.NAME, "password").send_keys("1234567")

# Click the dropdown
driver.find_element(By.ID, "type-inputEl").click()
time.sleep(1)


# Choose Staff or Student
# For Student:
student_option = driver.find_element(
    By.XPATH, "//li[contains(@class,'x-boundlist-item') and text()='Student']"
)
student_option.click()

# Or select Staff:
# driver.find_element(
#     By.XPATH, "//li[contains(@class,'x-boundlist-item') and text()='Staff']"
# ).click()

time.sleep(4)
login_button = driver.find_element(By.ID, "btnLogin-btnInnerEl")
login_button.click()    
driver.close()
