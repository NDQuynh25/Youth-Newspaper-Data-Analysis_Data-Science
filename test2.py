import requests
from bs4 import BeautifulSoup

# URL của bài báo (thay đổi thành URL của bài báo bạn muốn lấy nội dung)
url = "https://tuoitre.vn/tai-lien-hiep-quoc-iran-to-israel-dung-bom-nang-hon-2-000kg-cua-my-de-khong-kich-lebanon-20240928064428659.htm"

# Gửi yêu cầu đến URL
response = requests.get(url)

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
