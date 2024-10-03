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


driver = webdriver.Chrome()

options = Options()
options.add_argument("--ignore-certificate-errors")  # Bỏ qua lỗi chứng chỉ SSL
options.add_argument("--allow-insecure-localhost")  # Cho phép localhost không an toàn

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Cuộn xuống trang để tải thêm dữ liệu
last_height = driver.execute_script("return document.documentElement.scrollHeight")
driver.get('https://tuoitre.vn/the-gioi/trang-180.htm')
sl = 0

max_clicks = 40  # Số lần nhấn tối đa

while True:
    # Cuộn xuống
    print(">>>", last_height)
    

    driver.execute_script("window.scrollTo(0, " + str(last_height) + ");")
    
    # Chờ để dữ liệu mới tải về
    time.sleep(4)  

    # Tính chiều cao mới của trang
    new_height = driver.execute_script("return document.documentElement.scrollHeight")

    print(">>>", new_height)
    if new_height == last_height:
        if sl == max_clicks:
            break

        load_more_button = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.XPATH, '//a[text()="Xem thêm"]'))
)
        

        # Cuộn đến nút "Xem thêm"
        driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
        time.sleep(2)  # Thêm thời gian chờ ngắn trước khi nhấn

        print(">>> Nhấn nút Xem thêm ", sl)
        load_more_button.click()
        sl+=1
        last_height = new_height
        
    last_height = new_height

articles = set()

articles = driver.find_elements(By.CSS_SELECTOR, 'a.box-category-link-with-avatar.img-resize')




for article in articles:
    title = article.get_attribute('title')
    link = article.get_attribute('href')
    print(f"Title: {title}, Link: {link}")


with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Text', 'Link'])
    
    for article in articles:
        title = article.get_attribute('title')
        link = article.get_attribute('href')
        writer.writerow([title, link])
# Đóng trình duyệt
driver.quit()



def getDetails(link):  
   
    # Gửi yêu cầu đến URL
    response = requests.get(link)

    # Kiểm tra xem yêu cầu có thành công không
    if response.status_code == 200:
        # Phân tích nội dung HTML của trang
        soup = BeautifulSoup(response.text, 'html.parser')

        # Thể loại
        category = soup.find('div', class_='detail-cate').text.strip()
        print(f"Thể loại: {category}")

        # Lấy tiêu đề bài báo
        title = soup.find('h1', class_='detail-title article-title').text.strip()
        print(f"Tiêu đề: {title}")

        # Lấy tóm tắt bài báo
        summary = soup.find('h2', class_='detail-sapo').text.strip()
        print(f"Tóm tắt: {summary}")

        # Lấy nội dung bài báo 
        author = soup.find('a', class_='name').text.strip()
        print(f"Tác giả: {author}")

        # Thời gian đăng
        publish_date = soup.find('div', class_='detail-time').text.strip()
        print(f"Thời gian đăng: {publish_date}")
        
        # Loại bỏ các phần tử không cần thiết
        tags = []
        tags += soup.find_all('figcaption')
        tags += soup.find_all('div', class_='VCSortableInPreviewMode')
        if tags:
            [tag.decompose() for tag in tags]

        # Nội dung bài báo
        content = soup.find('div', class_='detail-content afcbc-body').text.strip()
        print(f"Nội dung: {content}")



    else:
        print(f"Không thể truy cập trang, mã lỗi: {response.status_code}")
