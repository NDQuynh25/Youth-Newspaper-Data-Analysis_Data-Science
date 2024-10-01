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

# Thiết lập Selenium với các tùy chọn
options = Options()
options.add_argument("--ignore-certificate-errors")  # Bỏ qua lỗi chứng chỉ SSL
options.add_argument("--allow-insecure-localhost")  # Cho phép localhost không an toàn
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Truy cập trang web
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
            winsound.Beep(1000, 5000)  # Tần số 1000Hz trong 500ms (0.5 giây)
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

# Tạo danh sách để lưu thông tin bài báo
articles_data = []








# Hàm để lấy thông tin chi tiết từ link bài báo
def get_details(link):
    details = {}
    # Gửi yêu cầu đến URL
    response = requests.get(link)

    # Kiểm tra xem yêu cầu có thành công không
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Lấy thông tin cần thiết
        details['category'] = clean_text(soup.find('div', class_='detail-cate').text.strip()) if soup.find('div', class_='detail-cate') else "Không có thể loại"
        details['summary'] = clean_text(soup.find('h2', class_='detail-sapo').text.strip()) if soup.find('h2', class_='detail-sapo') else "Không có tóm tắt"
        details['author'] = clean_text(soup.find('a', class_='name').text.strip()) if soup.find('a', class_='name') else "Không có tác giả"
        details['publish_date'] = clean_text(soup.find('div', class_='detail-time').text.strip()) if soup.find('div', class_='detail-time') else "Không có thời gian đăng"
        
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
            content = ' '.join([clean_text(p.text) for p in paragraphs])  # Nối các đoạn với dấu cách
            details['content'] = content if content else "Không có nội dung"
        else:
            details['content'] = "Không có nội dung"
    else:
        print(f"Không thể truy cập trang, mã lỗi: {response.status_code} , link: {link}")


    
    return details


def clean_text(text):
    # Loại bỏ dấu ngoặc kép và các ký tự không mong muốn khác nếu cần
    #cleaned_text = text.replace('"', '').strip()  # Loại bỏ dấu ngoặc kép
    clean_text
    return text



# Lặp qua từng bài báo để lấy thông tin chi tiết
for article in articles:
    title = article.get_attribute('title')
    link = article.get_attribute('href')
    
    
    if link.startswith('https://tuoitre.vn/'):
        print(f"Đang lấy thông tin bài báo: {title}")
        details = get_details(link)
        details['title'] = title
        details['link'] = link  #
        articles_data.append(details)  

# Ghi thông tin vào file CSV
with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link', 'Category', 'Summary', 'Author', 'Publish Date', 'Content'])  
    
    for article in articles_data:
        writer.writerow([article['title'], article['link'], article['category'], article['summary'], article['author'], article['publish_date'], article['content']])

# Đóng trình duyệt sau khi hoàn thành
driver.quit()


