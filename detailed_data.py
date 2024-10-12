import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Tùy chọn trình duyệt
options = Options()
options.add_argument("--ignore-certificate-errors")  # Bỏ qua lỗi chứng chỉ SSL
options.add_argument("--allow-insecure-localhost")  # Cho phép localhost không an toàn
options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình
options.add_argument("--disable-extensions")  # Vô hiệu hóa các tiện ích mở rộng
current_row = 0 
start_row = 0 
print(">>> Đang mở tệp CSV...") 



with open('1_output.csv', mode='r', newline='', encoding='utf-8') as file:

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
   
    reader = csv.reader(file)
    next(reader)  # Bỏ qua dòng tiêu đề
    
    with open('2_output_details.csv', 'a', newline='', encoding='utf-8-sig') as output_file:
        
        writer = csv.writer(output_file)
        writer.writerow(['Title', 'Link', 'Category', 'Summary', 'Author', 'Publish Date', 'Start', 'Content'])
        
        print(">>> Bắt đầu lấy dữ liệu chi tiết từ các bài viết...")
        for row in reader:
            current_row += 1
            if current_row < start_row:
                continue  
            title = row[0]
            link = row[1]

            driver.get(link)

            # Chờ trang tải (tùy chỉnh thời gian này nếu cần)
            time.sleep(1.5)

            # Lấy nội dung trang HTML
            html = driver.page_source

            # Phân tích nội dung HTML với BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Lấy thông tin từ trang web, với kiểm tra lỗi
          
            try:
                start = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'showtotalreactuser'))
                ).text.strip()
                if "Trở thành người đầu tiên tặng sao" in start:
                    start = "0 đánh giá"  # Hoặc giá trị khác mà bạn muốn đặt khi không có đánh giá
            except:
                start = None
            try:
                category = soup.find('div', class_='detail-cate').text.strip()
            except AttributeError:
                category = None
            try:
                summary = soup.find('h2', class_='detail-sapo').text.strip()
            except AttributeError:
                summary = None
            try:
                author = soup.find('a', class_='name').text.strip()
            except AttributeError:
                author = None
            try:
                publish_date = soup.find('div', class_='detail-time').text.strip()
            except AttributeError:
                publish_date = None
            

            # Loại bỏ các phần tử không cần thiết
            tags = []
            tags += soup.find_all('figcaption')
            tags += soup.find_all('div', class_='VCSortableInPreviewMode')
            if tags:
                [tag.decompose() for tag in tags]

            # Lấy nội dung bài báo
            try:
                content = soup.find('div', class_='detail-content afcbc-body').text.strip()
            except AttributeError:
                content = "N/A"
           
            print(f"Điểm bài viết: {start}")
            
            print()
            # Ghi dữ liệu vào tệp CSV
            writer.writerow([title, link, category, summary, author, publish_date, start, content])
            
    driver.quit()

