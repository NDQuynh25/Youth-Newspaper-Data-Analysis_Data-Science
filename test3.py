from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import httpx
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException






# Thiết lập Selenium với các tùy chọn
options = Options()
options.add_argument("--ignore-certificate-errors")  
options.add_argument("--allow-insecure-localhost")  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Mở trang web
driver.get('https://tuoitre.vn/the-gioi.htm')


last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Chờ để dữ liệu mới tải về
    time.sleep(2)  
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:   
        break
    last_height = new_height

articles = driver.find_elements(By.CSS_SELECTOR, 'a.box-category-link-with-avatar.img-resize')


for article in articles:
    link = article.get_attribute('href')
    title = article.get_attribute('title')
    print(f"Tiêu đề: {title}", f"Link: {link}")

with open('output.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow([title, link])
    for article in articles:
        link = article.get_attribute('href')
        title = article.get_attribute('title')
        writer.writerow([title, link])
driver.quit()


