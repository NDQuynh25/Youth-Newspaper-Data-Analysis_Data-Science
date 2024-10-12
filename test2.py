from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Thiết lập Selenium với các tùy chọn
options = Options()
options.add_argument("--ignore-certificate-errors")  
options.add_argument("--allow-insecure-localhost")  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL của bài báo
url = "https://tuoitre.vn/tai-lien-hiep-quoc-iran-to-israel-dung-bom-nang-hon-2-000kg-cua-my-de-khong-kich-lebanon-20240928064428659.htm"

# Mở trang web
driver.get(url)

# Chờ trang tải (tùy chỉnh thời gian này nếu cần)
time.sleep(3)

# Lấy nội dung trang HTML
html = driver.page_source

# Phân tích nội dung HTML với BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Thể loại
category = soup.find('div', class_='detail-cate').text.strip()
print(f"Thể loại: {category}")

# Lấy tiêu đề bài báo
title = soup.find('h1', class_='detail-title article-title').text.strip()
print(f"Tiêu đề: {title}")

# Lấy tóm tắt bài báo
summary = soup.find('h2', class_='detail-sapo').text.strip()
print(f"Tóm tắt: {summary}")

# Lấy tác giả bài báo
author = soup.find('a', class_='name').text.strip()
print(f"Tác giả: {author}")

# Thời gian đăng
publish_date = soup.find('div', class_='detail-time').text.strip()
print(f"Thời gian đăng: {publish_date}")

# Điểm bài viết
start = soup.find('span', class_='showtotalreactuser').text.strip()
print(f"Điểm bài viết: {start}")

# Loại bỏ các phần tử không cần thiết
tags = []
tags += soup.find_all('figcaption')
tags += soup.find_all('div', class_='VCSortableInPreviewMode')
if tags:
    [tag.decompose() for tag in tags]

# Nội dung bài báo
content = soup.find('div', class_='detail-content afcbc-body').text.strip()
print(f"Nội dung: {content}")

# Đóng trình duyệt
driver.quit()
