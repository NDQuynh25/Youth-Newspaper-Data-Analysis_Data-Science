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



# Hàm để lấy thông tin chi tiết từ link bài báo
def get_details(link):
    retries = 3
    details = {}

    for _ in range(retries):
        response = None
        try:
            response = httpx.get(link, timeout=10)
        except httpx.RequestError as e:
            continue

        # Kiểm tra xem yêu cầu có thành công không
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Lấy thông tin cần thiết
            details['category'] =soup.find('div', class_='detail-cate').text.strip() if soup.find('div', class_='detail-cate') else "Không có thể loại"
            details['summary'] = soup.find('h2', class_='detail-sapo').text.strip() if soup.find('h2', class_='detail-sapo') else "Không có tóm tắt"
            details['author'] = soup.find('a', class_='name').text.strip() if soup.find('a', class_='name') else "Không có tác giả"
            details['publish_date'] = soup.find('div', class_='detail-time').text.strip() if soup.find('div', class_='detail-time') else "Không có thời gian đăng"
            
            # Loại bỏ các phần tử không cần thiết
            tags = []
            tags += soup.find_all('figcaption')
            tags += soup.find_all('div', class_='VCSortableInPreviewMode')
            if tags:
                [tag.decompose() for tag in tags]

            # Nội dung bài báo
            # Lấy nội dung bài báo từ nhiều đoạn văn và nối chúng với dấu cách
            content_div = soup.find('div', class_='detail-content afcbc-body')
            if content_div:
                paragraphs = content_div.find_all('p')  # Tìm tất cả các thẻ <p>
                content = ' '.join([(p.text.strip()) for p in paragraphs])  # Nối các đoạn với dấu cách
                details['content'] = content if content else "Không có nội dung"
            else:
                details['content'] = "Không có nội dung"
            return details
        else:
            print(f"Không thể truy cập trang, mã lỗi: {response.status_code} , link: {link}")
            
    
    return None


    
    








# Thiết lập Selenium với các tùy chọn
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
            current_url = driver.current_url
            print(">>> current_url: ", current_url)
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


# Lấy tất cả bài báo sau khi cuộn
articles = driver.find_elements(By.CSS_SELECTOR, 'a.box-category-link-with-avatar.img-resize')


with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link', 'Category', 'Summary', 'Author', 'Publish Date', 'Content'])  
    for article in articles:
        try:
            #article = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.box-category-link-with-avatar.img-resize')))
            title = article.get_attribute('title') if article.get_attribute('title') else "Không có tiêu đề"
            link = article.get_attribute('href')
            if link.startswith('https://tuoitre.vn/'):
                print(f"Title: {title}, Link: {link}")
                writer.writerow([title, link])
        except StaleElementReferenceException:
            print("Lỗi StaleElementReferenceException, thử lại...")
            # Thử tìm lại phần tử và lấy thông tin một lần nữa
            #articles = driver.find_elements(By.CSS_SELECTOR, 'a.box-category-link-with-avatar.img-resize')
            continue  # Tiếp tục vòng lặp để thử lại với phần tử tiếp theo
        except Exception as e:
            print(f"Lỗi: {e}")

driver.quit()


# Lấy thông tin chi tiết từ các bài báo
with open('output.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Bỏ qua dòng tiêu đề

    with open('output_details.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link', 'Category', 'Summary', 'Author', 'Publish Date', 'Content'])
        
        for row in reader:
            title, link = row
            details = get_details(link)
            if details:
                print(f"Title: {title}, Link: {link}")
                print(details)
                writer.writerow([title, link, details['category'], details['summary'], details['author'], details['publish_date'], details['content']])
            else:
                print(f"Không thể lấy thông tin chi tiết từ bài báo: {title}, {link}")