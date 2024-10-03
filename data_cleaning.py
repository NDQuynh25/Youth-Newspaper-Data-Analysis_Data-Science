import csv


def clean_content(content):
    content = content.replace('\n', ' ')  # Loại bỏ các ký tự xuống dòng
    content = content.replace('\t', ' ')  # Loại bỏ các ký tự tab
    content = content.replace('\r', ' ')  # Loại bỏ các ký tự carriage return
    content = content.lower()             # Chuyển tất cả về chữ thường

    return content

with open('output_details.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Bỏ qua dòng tiêu đề

    with open('output_cleaned.csv', mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link', 'Category', 'Summary', 'Author', 'Publish Date', 'Content'])
        
        for row in reader:
            title = clean_content(row[0])
            link = row[1]
            category = clean_content(row[2])
            summary = clean_content(row[3])
            author = clean_content(row[4])
            publish_date = clean_content(row[5])
            content = clean_content(row[6])
            
            # Loại bỏ các ký tự không cần thiết trong nội dung bài báo
            #print(f"Title: {title}, Link: {link}")
            writer.writerow([title, link, category, summary, author, publish_date, content])
        print(">>> Đã lưu thông tin chi tiết bài báo vào tệp output_details_cleaned.csv")