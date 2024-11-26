# -*- coding: utf-8 -*-
import re
import unicodedata
from pyvi import ViTokenizer, ViPosTagger
import gensim
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.summarization import summarize

# Tải danh sách từ dừng
with open('vietnamese-stopwords.txt', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

# Chuẩn hóa Unicode
def normalize_unicode(text):
    return unicodedata.normalize('NFC', text)

# Tóm tắt văn bản




def stop_words(text):   
    words = [word for word in text.split() if word not in stopwords]
    return ' '.join(words)

def summarize_(text):
    return text

def preprocess_text(text):
    text = normalize_unicode(text)   # Chuẩn hóa Unicode
    text = text.lower()              # Chuyển chữ thường
    text = re.sub(r'[^\w\s]', ' ', text)  # Loại bỏ ký tự đặc biệt
    text = ViTokenizer.tokenize(text)    # Tách từ tiếng Việt
    return text
   
for i in range(1, 51):
    with open(f'data_raw\\crawling_{i}.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Bỏ qua dòng tiêu đề
        with open(f'preprocessed_data\\preprocessed_{i}.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Link', 'Title', 'Description', 'Content', 'Category', 'Author', 'Publish Date', 'Start'])
            for row in reader:
                link = row[0]
                title = stop_words(preprocess_text(row[1]))
                description = stop_words(preprocess_text(row[2]))
                content = stop_words(preprocess_text(summarize_(row[3])))
                category = preprocess_text(row[4])
                author = preprocess_text(row[5])
                publish_date = row[6]
                start = row[7]
                writer.writerow([link, title, description, content, category, author, publish_date, start])

