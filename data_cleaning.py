import csv
import re



# Further expanding the Vietnamese stopwords list
vietnamese_stopwords = set([
    "và", "là", "của", "có", "với", "cho", "đã", "được", "ở", "trên", "tại", "một", 
    "các", "như", "vì", "lúc", "nên", "đến", "còn", "để", "vẫn", "khi", "bởi", "ra", 
    "thì", "lại", "này", "nọ", "đó", "kia", "vậy", "tôi", "anh", "chị", "ông", "bà", 
    "họ", "chúng", "ta", "mình", "nó", "nếu", "rồi", "gì", "ai", "đi", "vào", "hết", 
    "đây", "đó", "vừa", "đang", "nhưng", "rất", "cùng", "cũng", "hơn", "sau", "trước", 
    "còn", "chỉ", "có thể", "nào", "thế", "như", "làm", "thấy", "vừa", "cùng", "cũng", 
    "này", "đi", "gì", "mà", "lên", "xuống", "tại", "vậy", "này", "khi", "cả", "lần", 
    "đang", "giữa", "đâu", "ai", "gì", "từ", "trong", "ngoài", "hết", "nếu", "còn", 
    "bởi vì", "với", "tuy", "trên", "không", "rằng", "dưới", "bằng", "hay", "do", 
    "hoặc", "ở", "trước", "nên", "mà", "cũng", "nhưng", "vì", "đã", "là", "chỉ", 
    "thì", "bị", "được", "của", "về", "tất cả", "bằng cách", "nhằm", "thế nào", "tuy nhiên",
    "bởi vì", "cho đến", "vẫn", "trong khi", "ngay cả", "nhờ vào", "sau đó", "hoặc là", 
    "hơn nữa", "dù cho", "một cách", "liên quan", "tùy theo", "ngay sau", "càng", "cũng như",
    "tuyệt đối", "rõ ràng", "một số", "hầu hết", "thông qua", "đồng thời", "gần như", "chắc chắn", 
    "đặc biệt", "bởi", "kể cả", "hoàn toàn", "tương đối", "nhiều khi", "kể từ", "từng", "điều đó", 
    "như vậy", "có thể", "đôi khi", "vừa mới", "đầu tiên", "liên tục", "cách đây", "theo đó", 
    "do đó", "mỗi", "tuy", "cũng như", "mặc dù", "trong đó", "giả sử", "trên thực tế", "chủ yếu", 
    "sau này", "hầu như", "thông thường", "trên hết", "tất nhiên", "vấn đề", "vì vậy", "qua đó", 
    "thay vì", "ngoài ra", "tại sao", "ngay lập tức", "do vậy", "trong khi đó", "từ trước", "theo đó"
])

def remove_more_stopwords(text):
    
    
    
    
    # for word in text.split():
    #     if word in vietnamese_stopwords:
    #         text = text.replace(word, '')
    return text


def normalize_text(text):
    text = text.lower()
  
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('\xa0', ' ').strip()

    text = re.sub(r'[^\w\s]', '', text)

    text = ' '.join(text.split())

    return text


def normalize_start_value(start):
    if start == "":
        return 0
    elif start.lower() == "trở thành người đầu tiên tặng sao cho bài viết":
        return 0
    elif start.lower() == "na":
        return 0
    else:
        try:
            # Cố gắng lấy số lượng đánh giá từ chuỗi
            return int(start.split(" ")[0])
        except (ValueError, IndexError):
            # Trường hợp không thể chuyển đổi, trả về 0
            return 0
        
with open('2_output_details.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Bỏ qua dòng tiêu đề

    with open('3_output_cleaned.csv', mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link', 'Category', 'Summary', 'Author', 'Publish Date', 'Start', 'Content'])
        
        for row in reader:
            if row == []:
                continue
            title = remove_more_stopwords(normalize_text(row[0]))
            link = row[1]
            category = normalize_text(row[2])
            summary = remove_more_stopwords(normalize_text(row[3]))
            author = normalize_text(row[4])
            publish_date = normalize_text(row[5])
            start = normalize_start_value(normalize_text(row[6]))
            content = remove_more_stopwords(normalize_text(row[7]))

            writer.writerow([title, link, category, summary, author, publish_date, start, content])
        print(">>> Đã lưu thông tin chi tiết bài báo vào tệp output_details_cleaned.csv")
