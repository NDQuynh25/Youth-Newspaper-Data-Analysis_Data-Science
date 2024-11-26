import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Đọc dữ liệu
file_path = "preprocessed_data/preprocessed_all.csv"  # Đường dẫn đến file dữ liệu
data = pd.read_csv(file_path)

# Kết hợp các cột văn bản (Title, Description, Content)
data['combined_text'] = data['Title'] + " " + data['Description'] + " " + data['Content']

# Loại bỏ các dòng có giá trị NaN trong cột 'combined_text'
data = data.dropna(subset=['combined_text'])

# Mã hóa nhãn Category thành số
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
data['Category_encoded'] = label_encoder.fit_transform(data['Category'])

# Tách dữ liệu thành các biến đầu vào và nhãn
X = data['combined_text']
y = data['Category_encoded']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Biến đổi văn bản thành vector TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Xây dựng mô hình KNN
k = 5  # Số lượng láng giềng gần nhất
knn_model = KNeighborsClassifier(n_neighbors=k)

# Huấn luyện mô hình
knn_model.fit(X_train_tfidf, y_train)

# Dự đoán trên tập kiểm tra
y_pred = knn_model.predict(X_test_tfidf)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
print(f"KNN Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Dự đoán chủ đề cho một đoạn văn bản mới
new_text = "Enter your text here to classify"  # Đoạn văn bản mới để dự đoán
new_text_tfidf = tfidf_vectorizer.transform([new_text])
predicted_category_encoded = knn_model.predict(new_text_tfidf)
predicted_category = label_encoder.inverse_transform(predicted_category_encoded)
print(f"Predicted Category: {predicted_category[0]}")
