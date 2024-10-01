from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import winsound
# Cấu hình trình duyệt
options = Options()
options.add_argument("--ignore-certificate-errors")  # Bỏ qua lỗi chứng chỉ SSL
options.add_argument("--allow-insecure-localhost")  # Cho phép localhost không an toàn
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Mở trang web
driver.get('https://tuoitre.vn/the-gioi.htm')

# Cuộn xuống trang để tải thêm dữ liệu
last_height = driver.execute_script("return document.body.scrollHeight")

sl = 0
max_clicks = 40  # Số lần nhấn tối đa

while True:
    # Cuộn xuống
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Chờ để dữ liệu mới tải về
    time.sleep(2)  # Có thể điều chỉnh thời gian chờ

    # Tính chiều cao mới của trang
    new_height = driver.execute_script("return document.body.scrollHeight")
    print("Chiều cao mới:", new_height)

    if new_height == last_height:
        if sl == max_clicks:
            #winsound.Beep(1000, 5000) 
            break

        try:
            load_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//a[text()="Xem thêm"]'))
            )
            # Cuộn đến nút "Xem thêm" và nhấn
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            time.sleep(2)  # Thêm thời gian chờ ngắn trước khi nhấn
            load_more_button.click()
            print(">>> Nhấn nút Xem thêm lần ", sl)
            sl += 1
        except Exception as e:
            
            print(f"Không tìm thấy hoặc nhấn nút 'Xem thêm': {e}")
            break
    last_height = new_height

# Lấy danh sách bài viết
articles = driver.find_elements(By.CSS_SELECTOR, 'a.box-category-link-with-avatar.img-resize')

# In ra tiêu đề và liên kết
for article in articles:
    title = article.get_attribute('title')
    link = article.get_attribute('href')
    print(f"Title: {title}, Link: {link}")

# Lưu vào tệp CSV
with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Text', 'Link'])
    
    for article in articles:
        title = article.get_attribute('title')
        link = article.get_attribute('href')
        writer.writerow([title, link])

# Đóng trình duyệt
driver.quit()
