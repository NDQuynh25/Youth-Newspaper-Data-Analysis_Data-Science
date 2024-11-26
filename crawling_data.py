import os
import csv
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
import random
import requests


# Tùy chọn trình duyệt
options = Options()
options.add_argument("--ignore-certificate-errors")  # Bỏ qua lỗi chứng chỉ SSL
options.add_argument("--allow-insecure-localhost")  # Cho phép localhost không an toàn
options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình
options.add_argument("--disable-extensions")  # Vô hiệu hóa các tiện ích mở rộng
# Đường dẫn tới thư mục
input_file='raw_data/crawling_data.csv'

for i in range(49, 50):
    input_file = f'2_output_details.csv'

    with open(input_file, 'r', newline='', encoding='utf-8') as file:
        output_file_path = os.path.join('raw_data_1/', f'crawling_50.csv')
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
            reader = csv.reader(file)
            writer = csv.writer(output_file)
            writer.writerow(['Link', 'Title', 'Description', 'Content', 'Category',  'Author', 'Publish Date', 'Start']) # Ghi tiêu đề

            header = next(reader) # bỏ qua dòng tiêu đề
            
            
            # Duyệt từng dòng
            for row in reader:
                link = row[1]
                title = row[0]
                description = row[3]
                content = row[4]
                category = row[2]
                soup = None
                
                try :
                    req = requests.get(link)
                    
                    if req.status_code != 200:
                        print(f"Lỗi khi tải trang {link}: {req.status_code}")
                        continue
                    else:
                        soup = BeautifulSoup(req.text, 'html.parser')
                except requests.exceptions.RequestException as e:
                    print(f"Lỗi khi tải trang {link}: {e}")
                    continue

                start = random.randint(0, 100)


            
                try:
                    author = soup.find('div', class_='author-info').text.strip()
                except AttributeError:
                    author = None
                    continue

                try:
                    publish_date = soup.find('div', class_='detail-time').text.strip()
                except AttributeError:
                    publish_date = None
                    continue

                writer.writerow([link, title, description, content, category, author, publish_date, start])

    
