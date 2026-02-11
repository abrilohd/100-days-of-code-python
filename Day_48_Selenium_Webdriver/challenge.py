from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")



event_time = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")
event_name = driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")

events = {}
for n in range(len(event_name)):
    events[n] = {
        "time": event_time[n].text,
        "name": event_name[n].text
    }

print(events)

driver.close()