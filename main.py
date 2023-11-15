import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

s = Service(executable_path=r"D:\pythonProject4\test\chromedriver\chromedriver.exe")

url = "https://petfriends.skillfactory.ru/login"
driver = webdriver.Chrome(service=s)
email = "panfilivan279@gmail.com"
password = "8357"


try:
    driver.get(url=url)
    time.sleep(2)
    email_input = driver.find_element(By.ID, "email")
    email_input.click()
    time.sleep(2)
    email_input.send_keys(email)

    password_input = driver.find_element(By.ID, "pass")
    password_input.click()
    time.sleep(5)
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(5)

    navbar_toggler_icon = driver.find_element(By.XPATH, "/html/body/nav/button/span")
    navbar_toggler_icon.click()
    time.sleep(2)
    nav_link = driver.find_element(By.XPATH, "//*[@id='navbarNav']/ul/li[1]/a")
    nav_link.click()
    time.sleep(2)

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-text')

    for i in range(len(names)):
       assert images[i].get_attribute('src') != ''
       assert names[i].text != ''
       assert descriptions[i].text != ''
       assert ', ' in descriptions[i]
       parts = descriptions[i].text.split(", ")
       assert len(parts[0]) > 0
       assert len(parts[1]) > 0

    time.sleep(5)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
